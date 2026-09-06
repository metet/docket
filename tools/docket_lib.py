"""Shared Docket model. Imported by docket-lint and docket-index so the two
cannot disagree about validity or derived state (r008)."""
import os, re, datetime

PROTOCOLS = {"docket/0.1", "docket/0.2", "docket/0.3"}
CURRENT   = "docket/0.3"
# Versions in which a rule applies, named rather than derived from CURRENT.
# `proto == CURRENT` meant "0.2" only by accident; the next bump would have
# silently stopped enforcing it on every 0.2 filing already in the store,
# which immutability makes unfixable (r015, codex).
EVIDENCE_RULE = {"docket/0.2", "docket/0.3"}
# Versions a reader handles with reduced fidelity, and the only ones worth
# warning about. Not "anything older than CURRENT": filings are immutable, so
# "you should have used a newer version" is unactionable by construction, and
# keying it on CURRENT turned every one of the store's 0.2 filings into a
# warning the moment 0.3 landed -- 46 lines of noise that teach parties to
# stop reading lint. 0.1 stays listed because it genuinely reads worse: its
# filing ids carry no party (see id_of), so authorship is not recoverable.
LEGACY = {"docket/0.1"}
REQUIRED  = ["protocol", "id", "docket", "from", "type", "date"]
TYPES     = {"request", "filing", "disposition"}
ACTS      = {"question","task","review","report","answer","objection","ack","erratum"}
# An erratum may correct the record, never identity or state. Identity fields
# would be forgery; status/assignee already have authorised ways to change.
#
# `act` is deliberately absent. An erratum supplies a replacement as its own
# field, and an erratum's own `act` is necessarily "erratum" -- docket-new
# requires --act erratum before it will accept --corrects at all. So correcting
# `act` could only ever write "erratum". Listing it let a well-formed erratum
# silently falsify the filing it corrected, and left that filing failing
# validation for fields it was never going to have (r003/003). A mislabelled act
# is corrected by filing again with the right one, not by erratum.
# `to` was removed in 0.3 (r015). It is absent here rather than kept for old
# filings because no filing in any store ever corrected it: the only `corrects`
# on record names `act`. Dropping a field from this set can only make a past
# erratum ineffective, never invalid, and there is no such erratum.
CORRECTABLE = {"refs","evidence","blocked_on","parent","date"}
RETRACT_ONLY = {"date"}   # every filing has its own date; it cannot be replaced
# Naming one of these in `corrects` is an attempt to forge identity or to reach
# state without its authorised transition, so it invalidates the filing. Naming
# any other non-correctable field is merely ineffective, and warns.
PROTECTED = {"protocol", "id", "docket", "from", "type", "status", "assignee"}
STATUSES  = {"open","blocked","resolved","withdrawn"}
TERMINAL  = {"resolved","withdrawn"}

def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n")

def parties(store, include_retired=True):
    """Registered party names. Retired parties stay registered forever: filings
    are immutable, so removing a party would invalidate its history."""
    for p in (os.path.join(store,"PARTIES.md"), os.path.join(store,"..","PARTIES.md")):
        if os.path.exists(p):
            txt = read(p)
            active = txt.split("## Retired")[0]
            names = set(re.findall(r"^\|\s*`([a-z_][a-z0-9_-]*)`", active, re.M))
            if include_retired:
                names |= set(re.findall(r"^\|\s*`([a-z_][a-z0-9_-]*)`", txt, re.M))
            return names
    return set()

def scalar(v):
    """Strip an inline comment, then matching surrounding quotes."""
    v = re.sub(r"\s+#.*$", "", v).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v.strip()

def split_flow(s):
    """Split on commas that are not inside quotes.

    An item may legitimately contain a comma -- "docket-lint: 14 filings, 0
    errors" is one piece of evidence, not two. A plain split turned it into two,
    silently, in a filing that is immutable and lints clean either way. Quoting
    is how such an item is written; this is the matching reader.
    """
    out, cur, q = [], [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q: q = None
        elif ch in "\"'":
            q = ch; cur.append(ch)
        elif ch == ",":
            out.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out

def quote_flow(x):
    """Quote a flow-list item that would otherwise be split on its own comma."""
    x = str(x)
    if "," not in x: return x
    if '"' not in x: return f'"{x}"'
    if "'" not in x: return f"'{x}'"
    raise ValueError(f"cannot represent a list item containing a comma and "
                     f"both quote characters: {x!r}")

def as_list(v):
    """Inline flow style only: [a, b]. Block lists are rejected by front_matter."""
    if not v: return []
    if v.startswith("[") and v.endswith("]"):
        return [scalar(x) for x in split_flow(v[1:-1]) if x.strip()]
    return [v] if v else []

def front_matter(text):
    """Returns a dict, or None if absent. Raises ValueError on YAML we do not
    support, so it is never silently dropped."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: return None
    f = {}
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s", line):
            raise ValueError("block-style YAML lists are not supported; "
                             "use inline flow style, e.g. refs: [a.js, b.js]")
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if km: f[km.group(1)] = scalar(km.group(2))
    return f

FILING_RE = re.compile(r"^(\d{3})(?:-([a-z0-9_-]+?))?(?:-([a-z0-9-]+))?\.md$")

def is_filing(fn):
    """Only NNN-prefixed .md files are filings. A README.md or NOTES.md sitting
    in a docket directory is documentation, not a filing."""
    return bool(FILING_RE.match(fn))

def load(dpath):
    """Return filings with parsed metadata, in canonical order. Non-filing
    markdown in the directory is ignored."""
    out = []
    for fn in sorted(os.listdir(dpath)):
        if not is_filing(fn): continue
        txt = read(os.path.join(dpath, fn))
        try:
            fm, err = front_matter(txt) or {}, None
        except ValueError as e:
            fm, err = {}, str(e)
        m = FILING_RE.match(fn)
        out.append(dict(fn=fn, text=txt, fm=fm, err=err,
                        num=m.group(1),
                        party=(m.group(2) if m.group(3) else None)))
    return canonical(out)

def canonical(filings):
    """Total order: (sequence, party). Never uses `date` -- dates are
    self-asserted, skew, and a party with no clock emits placeholders."""
    return sorted(filings, key=lambda f: (f["num"], f["party"] or ""))

def expected_id(did, num, party, proto):
    if num == "000": return f"{did}/000"
    if proto == "docket/0.1": return f"{did}/{num}"        # legacy
    if party is None: return None       # malformed filename; reported separately
    return f"{did}/{num}-{party}"

def parse_ref(ref):
    """Split a `refs` entry into (path, line). PROTOCOL 2.

    Splits on the LAST colon, and only when what follows it is digits. Without
    that guard the rule breaks the very case it exists for: a blind last-colon
    split turns `C:\\src\\file.js` into path `C`. With it, a path is only ever
    truncated where a real line number follows.

      index.html:41   -> ("index.html", 41)
      C:/src/x.js:41  -> ("C:/src/x.js", 41)
      C:\\src\\x.js     -> ("C:\\src\\x.js", None)
      host:/path      -> ("host:/path", None)
    """
    head, sep, tail = ref.rpartition(":")
    if sep and tail.isdigit():
        return head, int(tail)
    return ref, None

def title(text):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else "(untitled)"

def apply_errata(filings):
    """Apply act: erratum filings onto the records they supersede.

    Filings are immutable, so a factual mistake can never be edited out. An
    erratum is the append-only correction: it names a filing and the fields that
    are wrong, optionally supplying replacements. Validation and reduction then
    see the corrected record, so one bad filing cannot break a store forever.
    """
    counts = {}
    for f in filings:
        counts[f["fm"].get("id")] = counts.get(f["fm"].get("id"), 0) + 1
    # An ambiguous id cannot be corrected: which filing would the erratum mean?
    by_id = {f["fm"].get("id"): f for f in filings
             if f["fm"].get("id") and counts[f["fm"].get("id")] == 1}
    for f in filings:
        f["corrected"] = set()
    for f in canonical(filings):
        fm = f["fm"]
        if fm.get("act") != "erratum":
            continue
        tgt = by_id.get(fm.get("supersedes"))
        if tgt is None or tgt is f:
            continue
        if fm.get("from") != tgt["fm"].get("from"):
            continue                      # only the author may correct their own record
        for field in as_list(fm.get("corrects")):
            if field not in CORRECTABLE:
                continue
            if field in fm and field not in RETRACT_ONLY:
                tgt["fm"][field] = fm[field]
            else:
                tgt["fm"].pop(field, None)
            tgt["corrected"].add(field)
    return filings


def reduce_docket(filings, invalid=frozenset(), known=frozenset()):
    """Single authoritative reduction (PROTOCOL 3). Returns derived state plus
    any authority violations. Invalid filings never change derived state."""
    st = dict(requester=None, status="open", assignee=None, blocked_on=None,
              violations=[], count=len(filings))
    assigned_by = None          # filename of the last filing to name an assignee
    for f in filings:
        if f["fn"] in invalid: continue
        fm, who = f["fm"], f["fm"].get("from")
        if f["num"] == "000":
            st["requester"] = who
            st["status"]    = fm.get("status", "open")
            if fm.get("assignee"):
                st["assignee"] = fm["assignee"]
                assigned_by = f["fn"]
            continue
        if "assignee" in fm:
            if fm["assignee"] in ("", "none", "None"):
                if who in (st["requester"], st["assignee"]):
                    st["assignee"] = None            # relinquished
                    continue
            claiming_unclaimed = (st["assignee"] is None
                                  and fm.get("act") == "ack"
                                  and fm["assignee"] == who)
            if who in (st["requester"], st["assignee"]) or claiming_unclaimed:
                st["assignee"] = fm["assignee"]
                assigned_by = f["fn"]     # for waiting_on, below
            else:
                st["violations"].append(
                    f"{f['fn']}: {who} may not set assignee "
                    f"(requester={st['requester']}, assignee={st['assignee']})")
        s = fm.get("status")
        # An objection from the requester reopens a terminal docket even without
        # an explicit status, so a reopen cannot be silently lost.
        if not s and fm.get("act") == "objection" and who == st["requester"] \
                and st["status"] in TERMINAL:
            s = "open"
        if not s: continue
        if s in TERMINAL:
            ok = who == st["requester"] and fm.get("type") == "disposition"
            why = "only the requester may close, via type: disposition"
        elif s == "blocked":
            ok = who in (st["requester"], st["assignee"]); why = "only the requester or assignee may block"
        elif s == "open":
            ok = who in (st["requester"], st["assignee"]); why = "only the requester or assignee may reopen/unblock"
        else:
            ok, why = False, f"unknown status {s!r}"
        if ok:
            st["status"] = s
            st["blocked_on"] = fm.get("blocked_on") if s == "blocked" else None
        else:
            st["violations"].append(f"{f['fn']}: {who} set status={s} without authority ({why})")
    valid = [f for f in filings if f["fn"] not in invalid]
    if st["status"] in TERMINAL or not valid:
        st["waiting_on"] = None
    elif st["status"] == "blocked" and st["blocked_on"] and known:
        # `blocked_on` is "a party or an external condition" with nothing to tell
        # them apart, so the registry decides: a name in it is a party, and that
        # party is who to run. Anything else is a condition no party can advance,
        # and naming one anyway invited someone to work on a blocked docket.
        # Registry membership rather than a syntax prefix, because a prefix is
        # another rule the weakest party has to remember (r002).
        st["waiting_on"] = st["blocked_on"] if st["blocked_on"] in known else None
    elif not st["assignee"]:
        # Unclaimed. Naming nobody is the point: r008 gives these their own
        # section, because with three parties every party assuming another has
        # it is the dominant failure mode (PROTOCOL 4). Unchanged by r014.
        last = valid[-1]["fm"].get("from")
        st["waiting_on"] = None if last == st["requester"] else st["requester"]
    else:
        # Pull-only: nothing wakes a party, so name whose turn it is. The
        # assignee owes work unless it has already spoken since it was assigned
        # AND since the requester last spoke; otherwise the requester owes a
        # close or an objection.
        #
        # Keying on "was the last filer the requester" instead (the rule until
        # r014) is complete for two parties and has no third case. A handoff
        # named a new assignee and then pointed the scheduler at the requester,
        # who owed nothing, and no filing by a non-requester could recover it --
        # so only the requester could route work onward. With three parties that
        # made the weakest one responsible for routing between the two strongest.
        def last_from(party):
            return max((i for i, f in enumerate(valid)
                        if f["fm"].get("from") == party), default=-1)
        at = {f["fn"]: i for i, f in enumerate(valid)}
        since = max(at.get(assigned_by, -1), last_from(st["requester"]))
        # <= not <: a party claiming an unclaimed docket files AT the moment it
        # takes the work, and that filing cannot also be the one discharging it.
        st["waiting_on"] = (st["assignee"]
                            if last_from(st["assignee"]) <= since
                            else st["requester"])
    return st


def validate_docket(store, dirname, known=None):
    """The single source of validity. Returns (filings, invalid, errors,
    warnings, state).

    Both docket-lint and docket-index call this, so a filing that one considers
    invalid cannot be counted as valid by the other. PROTOCOL 3: invalid filings
    are excluded from reduction and never silently change derived state.
    """
    known  = parties(store) if known is None else known
    active = parties(store, include_retired=False)
    did    = dirname.split("-")[0]
    dp    = os.path.join(store, dirname)
    filings = apply_errata(load(dp))
    errors, warnings, invalid = [], [], set()

    if not os.path.isdir(os.path.join(store, ".seq", did)):
        warnings.append(f"{dirname}: no .seq/{did} reservation (allocation was not atomic)")
    if not any(f["fn"] == "000-request.md" for f in filings):
        errors.append(f"{dirname}: no 000-request.md")
    ids, seen_ids = set(), {}
    for f in filings:
        fid = f["fm"].get("id")
        if not fid: continue
        ids.add(fid)
        seen_ids.setdefault(fid, []).append(f["fn"])
    for fid, fns in seen_ids.items():
        if len(fns) > 1:
            errors.append(f"{dirname}: id {fid} is claimed by {len(fns)} filings "
                          f"({', '.join(sorted(fns))}) — a party MUST NOT reuse a "
                          "sequence number it has already used in this docket")
            invalid.update(fns)

    for f in filings:
        fn, fm, w = f["fn"], f["fm"], f"{dirname}/{f['fn']}"
        errs = []
        if fm.get("act") == "erratum":
            sup = fm.get("supersedes")
            if not sup:
                errs.append("act: erratum requires supersedes")
            elif sup not in ids:
                errs.append(f"supersedes {sup!r} names no filing in this docket")
            else:
                tgt = next(t for t in filings if t["fm"].get("id") == sup)
                if tgt["fm"].get("from") != fm.get("from"):
                    errs.append("only the author of a filing may correct it; "
                                f"{sup} is {tgt['fm'].get('from')}'s")
            fields = as_list(fm.get("corrects"))
            if not fields:
                errs.append("act: erratum requires corrects: [<field>, ...]")
            for fld in fields:
                if fld in CORRECTABLE:
                    continue
                if fld in PROTECTED:
                    # Identity is forgery; state has authorised transitions of
                    # its own. Either is an attempt to route around a rule, so
                    # the filing is invalid and excluded from reduction.
                    errs.append(f"{fld!r} may not be corrected by erratum — "
                                "identity and state change only through their own "
                                "authorised paths")
                else:
                    # Merely uncorrectable, e.g. `act`, or a misspelled field.
                    # apply_errata skips it, so the record is unharmed. An error
                    # here would be permanent: the filing is immutable, so the
                    # store could never be clean again. docket-new refuses to
                    # write this, so conforming tooling cannot produce a new one.
                    warnings.append(f"{w}: {fld!r} is not correctable and was "
                                    f"ignored (allowed: {sorted(CORRECTABLE)})")
        def bad(m): errs.append(m)
        if f.get("err"): bad(f["err"])
        elif not fm:     bad("no YAML front matter")
        else:
            for k in REQUIRED:
                if k not in fm: bad(f"missing required field '{k}'")
            proto = fm.get("protocol")
            if proto not in PROTOCOLS: bad(f"unknown protocol {proto!r}")
            elif proto in LEGACY:
                warnings.append(f"{w}: {proto} reads with reduced fidelity; "
                                f"new filings should use {CURRENT}")
            if f["num"] == "000":
                if fn != "000-request.md": bad("the request MUST be named 000-request.md")
                if fm.get("type") != "request": bad("filing 000 must be type=request")
            else:
                if not f["party"]:
                    bad(f"filename MUST be <NNN>-<party>-<label>.md, here "
                        f"{f['num']}-{fm.get('from','<party>')}-"
                        f"{fm.get('act') or fm.get('type','filing')}.md "
                        f"(docket-new derives this; it is not meant to be typed)")
                elif known and f["party"] not in known:
                    bad(f"filename party {f['party']!r} is not registered")
                elif f["party"] != fm.get("from"):
                    bad(f"filename party {f['party']!r} disagrees with from: {fm.get('from')!r}")
            exp = expected_id(did, f["num"], f["party"], proto)
            if exp and fm.get("id") != exp: bad(f"id {fm.get('id')!r} should be {exp!r}")
            if fm.get("docket") != did: bad(f"docket {fm.get('docket')!r} should be {did!r} (no slug)")
            if fm.get("type") not in TYPES: bad(f"type {fm.get('type')!r} invalid")
            if "act" in fm and fm["act"] not in ACTS: bad(f"act {fm['act']!r} invalid")
            if fm.get("status") and fm["status"] not in STATUSES: bad(f"status {fm['status']!r} invalid")
            if known and fm.get("from") not in known: bad(f"from {fm.get('from')!r} not in PARTIES.md")
            elif active and fm.get("from") and fm.get("from") not in active:
                warnings.append(f"{w}: {fm['from']} is retired; its filings remain valid "
                                "but it should not file anything new")
            asg = fm.get("assignee")
            if asg and asg not in ("none","None") and known and asg not in known:
                bad(f"assignee {asg!r} is not a registered party")
            for r in as_list(fm.get("refs")):
                path, line = parse_ref(r)
                if not path: bad(f"refs entry {r!r} has no path")
                elif line is not None and line < 1:
                    bad(f"refs entry {r!r} has line {line}; lines are 1-based")
            if fm.get("status") == "blocked" and not fm.get("blocked_on"):
                bad("status: blocked requires blocked_on")
            if fm.get("type") == "disposition" and proto in EVIDENCE_RULE:
                ev = as_list(fm.get("evidence"))
                if not ev:
                    warnings.append(f"{w}: disposition carries no evidence (SHOULD)")
                elif all((dirname in parse_ref(e)[0] or parse_ref(e)[0].startswith(did + "/"))
                         for e in ev):
                    bad("a disposition's evidence must not consist solely of filings "
                        "from its own docket — evidence points outward (a commit sha, "
                        "command output, or a file outside the store)")
            par = fm.get("parent")
            if par:
                if not par.startswith(did + "/"): bad(f"parent {par!r} is not in this docket")
                elif par not in ids:              bad(f"parent {par!r} names no filing in this docket")
            # A plain calendar date is accepted alongside the full timestamp.
            # Canonical order is (NNN, party) and explicitly does not use `date`
            # (PROTOCOL §"Canonical order"), which already anticipates that "a
            # party with no clock may emit a placeholder". Requiring a precision
            # the party does not have produced exactly that: a fabricated
            # midnight, which the warning below then flags. A date that says only
            # what is known is the more truthful record (r010).
            raw, dt = fm.get("date", ""), None
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
                try:
                    dt = datetime.datetime.strptime(raw, fmt)
                    break
                except ValueError:
                    pass
            if dt is None:
                bad(f"date {raw!r} is neither RFC 3339 UTC "
                    f"(2026-08-29T15:41:00Z) nor a calendar date (2026-08-29)")
            else:
                now = datetime.datetime.now(datetime.timezone.utc)
                # A plain date is compared by day: today's date is not "future".
                future = (dt.date() > now.date() if len(raw) == 10 else
                          dt.replace(tzinfo=datetime.timezone.utc) > now)
                if future:
                    warnings.append(f"{w}: date {raw} is in the future")
                if raw.endswith("T00:00:00Z"):
                    warnings.append(f"{w}: date {raw} is exactly midnight — "
                                    f"likely a placeholder; write just the date "
                                    f"if the time is not known")
        if errs:
            invalid.add(fn)
            errors.extend(f"{w}: {m}" for m in errs)

    state = reduce_docket(filings, invalid, known)
    errors.extend(f"{dirname}/{v}" for v in state["violations"])
    return filings, invalid, errors, warnings, state


def dockets(store):
    """Docket directory names, in order."""
    return [d for d in sorted(os.listdir(store))
            if os.path.isdir(os.path.join(store, d)) and re.match(r"^r\d{3}", d)]

def workspaces_config_path():
    """Path to the workspaces configuration file.
    Checks DOCKET_WORKSPACES_FILE environment variable, then:
      ~/.config/docket/workspaces      (plain text list of paths, one per line)
      ~/.config/docket/workspaces.json (JSON: {"workspaces": [...]})
    """
    env = os.environ.get("DOCKET_WORKSPACES_FILE")
    if env:
        return os.path.abspath(env)
    cfg_dir = os.path.expanduser("~/.config/docket")
    txt = os.path.join(cfg_dir, "workspaces")
    js  = os.path.join(cfg_dir, "workspaces.json")
    if os.path.exists(txt):
        return txt
    if os.path.exists(js):
        return js
    return txt

def load_workspaces():
    """List of absolute workspace paths configured by the user.
    Supports plain text (one path per line, # comments ignored) or JSON.
    """
    path = workspaces_config_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        if path.endswith(".json") or content.startswith("{") or content.startswith("["):
            import json
            data = json.loads(content)
            ws = data.get("workspaces", []) if isinstance(data, dict) else data
            return [os.path.abspath(os.path.expanduser(p)) for p in ws if isinstance(p, str) and p.strip()]
        lines = []
        for line in content.splitlines():
            line = line.split("#")[0].strip()
            if line:
                lines.append(os.path.abspath(os.path.expanduser(line)))
        return lines
    except Exception:
        return []

def save_workspaces(paths):
    """Save the list of workspace paths to the configured file."""
    path = workspaces_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cleaned = []
    for p in paths:
        p_abs = os.path.abspath(os.path.expanduser(p))
        if p_abs not in cleaned:
            cleaned.append(p_abs)
    if path.endswith(".json"):
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"workspaces": cleaned}, f, indent=2)
            f.write("\n")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Docket trusted workspaces (one path per line)\n")
            for p in cleaned:
                f.write(f"{p}\n")

def match_workspace(target_path):
    """Find the configured workspace that contains target_path (if any)."""
    # macOS exposes /var through /private/var, and Windows paths are
    # case-insensitive. Compare canonical keys so the same directory cannot
    # fail allowlist matching merely because the client used another spelling.
    target = os.path.realpath(os.path.abspath(os.path.expanduser(target_path)))
    target_key = os.path.normcase(target)
    best_match = None
    for configured in load_workspaces():
        ws = os.path.realpath(configured)
        ws_key = os.path.normcase(ws)
        prefix = ws_key if ws_key.endswith(os.sep) else ws_key + os.sep
        if target_key == ws_key or target_key.startswith(prefix):
            if best_match is None or len(ws) > len(best_match):
                best_match = ws
    return best_match
