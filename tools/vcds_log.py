"""Drive VCDS to log measuring blocks of the engine ECU, and reconnect by itself.

    python tools/vcds_log.py --groups 014 001 003 --out "C:/Users/.../Downloads/x.CSV"

Opens 01-Motor, measuring blocks, the given groups (up to three) and the log
dialog, and logs to --out. When the ECU stops answering -- the ignition
switched off, the voltage dip of a start -- VCDS shows "Initialisation of
the control unit" with a single OK. This script presses it, goes back in and
logs on into the next file, --out with -2, -3 ... before the extension.
VCDS writes a log to disk only when its log dialog closes, so every part
that ends is a complete file.

    python tools/vcds_log.py --faults "C:/Users/.../Downloads/faults.txt"

reads the engine's fault memory instead (02), prints it and writes it to
the file, then goes back. Clearing it stays the owner's, by hand.

Every run ends by ending the communication with 01 (06) and closing VCDS,
and prints DONE, so nothing is left for the owner to click (--keep-open
leaves both open).

Stop a log by creating the file named by --stop (default --out + ".stop"), or
with --seconds. Either way the log dialog is stopped and closed, which is
what writes the last file.

**READ ONLY, by construction** (CLAUDE.md, *When Claude drives VCDS*): every
click goes through click(), which refuses any control not in ALLOWED. The
buttons that write to a control unit -- clear codes, basic settings,
coding, adaptation, output tests -- are named in FORBIDDEN as well, so the
refusal is explicit, not an accident of omission. The fault memory is the
owner's to clear, by hand.

Needs pywinauto (Windows only) and VCDS at VCDS_EXE. VCDS is a 32-bit
program; 64-bit Python warns about it and works.
"""

import argparse
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")

VCDS_EXE = r"C:\Auto-diagnostika\VCDS.exe"
VCDS_DIR = r"C:\Auto-diagnostika"

# Window titles, as regular expressions. VCDS here is Czech, and the
# accented letters come through the ANSI API inconsistently, so they are
# matched with a dot.
T_MAIN = r"VCDS:.*Hlavn.*"
T_SELECT = r".*V.b.r ..d.c. jednotky"
T_FUNCS = r".*01-Motor.*V.b.r funkc.*"
T_BLOCKS = r".*01-Motor.*M..en. hodnoty.*"
T_FAULTS = r".*01-Motor.*Pam.. z.vad.*"
T_INIT = r"VCDS: Inicializace jednotky"   # "the unit does not answer", OK only

# (window, control id) pairs this script may click, and nothing else.
ALLOWED = {
    ("select", "01-Motor"),      # the unit button, found by its text
    ("funcs", 1096),             # Mereni hodnoty - 08
    ("funcs", 1095),             # Pamet zavad - 02: opens the list, reads only
    ("faults", 1),               # Zpet
    ("funcs", 1301),             # Ukonceni komunikace - 06
    ("blocks", 1174), ("blocks", 1128), ("blocks", 1129),   # Start, groups A-C
    ("blocks", 1217),            # Logovani
    ("blocks", 1),               # Zpet
    ("log", 1256),               # Start
    ("log", 1257),               # Stop
    ("log", 1),                  # Zpet -- closing the dialog writes the file
    ("init", 2),                 # OK on "the unit does not answer"
    ("main", 1017),              # Vybrat jednotku
    ("select", 1249),            # Zpet
    ("main", 1026),              # Konec -- quits VCDS
}
FORBIDDEN = {
    ("blocks", 1293),            # Smazat chyby -- clears the fault memory
    ("faults", 1112),            # Vymazat pamet - 05 -- clears it too
    ("blocks", 1216),            # Prepnout na zakladni nastaveni
    ("log", 1260),               # Zakl. nastaveni
    ("funcs", 1102), ("funcs", 1104), ("funcs", 1101), ("funcs", 1100),
    ("funcs", 1103), ("funcs", 1107), ("funcs", 1308),
}

GROUP_EDITS = ((1135, 1174), (1136, 1128), (1137, 1129))
LOG_FILE_EDIT = 1046


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


class Vcds:
    def __init__(self):
        from pywinauto import Application
        self.Application = Application
        try:
            self.app = Application(backend="win32").connect(path=VCDS_EXE)
            log("VCDS already running")
        except Exception:
            self.app = Application(backend="win32").start(VCDS_EXE, work_dir=VCDS_DIR)
            log("VCDS started")
            time.sleep(6)
        for w in self.app.windows():
            if w.class_name() == "BalloonHelpClassDS":   # "a newer version"
                w.close()

    def win(self, title_re):
        return self.app.window(title_re=title_re)

    def exists(self, title_re):
        return self.win(title_re).exists(timeout=0.2)

    def log_dialog(self):
        for w in self.app.windows():
            if w.class_name() == "#32770" and w.window_text() == "":
                if any(c.control_id() == LOG_FILE_EDIT for c in w.descendants()):
                    return self.app.window(handle=w.handle)
        return None

    def click(self, where, spec, ctrl):
        if (where, ctrl) in FORBIDDEN or (where, ctrl) not in ALLOWED:
            raise RuntimeError("refused to click %s/%s: not on the read-only allow-list"
                               % (where, ctrl))
        if isinstance(ctrl, str):
            b = [c for c in spec.wrapper_object().descendants()
                 if c.class_name() == "Button" and c.is_visible()
                 and c.window_text().strip() == ctrl]
            if not b:
                raise RuntimeError("no visible button %r" % ctrl)
            b[0].click()
        else:
            spec.child_window(control_id=ctrl).click()

    def wait_enabled(self, spec, ctrl, timeout=40):
        """Wait for a button to become enabled; VCDS shows a window before
        its connection is up. Fails early if the unit stopped answering."""
        t0 = time.time()
        c = spec.child_window(control_id=ctrl)
        while time.time() - t0 < timeout:
            if self.exists(T_INIT):
                raise RuntimeError("the unit does not answer")
            try:
                if c.is_enabled():
                    return
            except Exception:
                pass
            time.sleep(0.5)
        raise RuntimeError("button %s never enabled" % ctrl)

    def open_blocks(self, groups):
        """From wherever VCDS is, to the measuring blocks showing `groups`."""
        self.stop_log()     # a log left open blocks the window's buttons
        if not self.exists(T_BLOCKS):
            if not self.exists(T_FUNCS):
                if not self.exists(T_SELECT):
                    self.click("main", self.win(T_MAIN), 1017)
                    time.sleep(2)
                self.click("select", self.win(T_SELECT), "01-Motor")
                self.win(T_FUNCS).wait("exists", timeout=40)
            self.wait_enabled(self.win(T_FUNCS), 1096)
            self.click("funcs", self.win(T_FUNCS), 1096)
            self.win(T_BLOCKS).wait("exists", timeout=20)
            time.sleep(2)
        blocks = self.win(T_BLOCKS)
        for (edit, start), g in zip(GROUP_EDITS, groups):
            self.wait_enabled(blocks, start)
            blocks.child_window(control_id=edit, class_name="Edit").set_edit_text(g)
            time.sleep(0.3)
            self.click("blocks", blocks, start)
            time.sleep(2.5)
        return blocks

    def read_faults(self):
        """The engine's fault list as VCDS shows it, one line per entry.
        Opens 02 and goes back; never touches 'Vymazat pamet'."""
        self.stop_log()
        if self.exists(T_BLOCKS):
            self.click("blocks", self.win(T_BLOCKS), 1)
            time.sleep(2)
        if not self.exists(T_FUNCS):
            if not self.exists(T_SELECT):
                self.click("main", self.win(T_MAIN), 1017)
                time.sleep(2)
            self.click("select", self.win(T_SELECT), "01-Motor")
            self.win(T_FUNCS).wait("exists", timeout=40)
        self.wait_enabled(self.win(T_FUNCS), 1095)
        self.click("funcs", self.win(T_FUNCS), 1095)
        fw = self.win(T_FAULTS)
        fw.wait("exists", timeout=30)
        self.wait_enabled(fw, 1)
        time.sleep(2)
        lines = fw.child_window(control_id=1110, class_name="ListBox").wrapper_object().item_texts()
        self.click("faults", fw, 1)
        time.sleep(1.5)
        return lines

    def start_log(self, blocks, path):
        self.wait_enabled(blocks, 1217)
        self.click("blocks", blocks, 1217)
        time.sleep(2)
        d = self.log_dialog()
        d.child_window(control_id=LOG_FILE_EDIT).set_edit_text(path)
        self.click("log", d, 1256)
        log("logging to %s" % path)

    def stop_log(self):
        d = self.log_dialog()
        if d is None:
            return
        try:
            self.click("log", d, 1257)
            time.sleep(1)
        except Exception:
            pass                       # already stopped
        self.click("log", d, 1)
        time.sleep(1.5)

    def end_session(self):
        """Back out of 01 and end the communication (06), so that nothing is
        left talking to the ECU. Called at the end of every run."""
        self.stop_log()
        if self.exists(T_FAULTS):
            self.click("faults", self.win(T_FAULTS), 1)
            time.sleep(1.5)
        if self.exists(T_BLOCKS):
            self.click("blocks", self.win(T_BLOCKS), 1)
            time.sleep(2)
        if self.exists(T_FUNCS):
            try:
                self.wait_enabled(self.win(T_FUNCS), 1301, timeout=10)
            except RuntimeError:
                pass
            self.click("funcs", self.win(T_FUNCS), 1301)
            time.sleep(2)
        if self.exists(T_FUNCS) or self.exists(T_BLOCKS):
            log("WARNING: the communication with 01 is still open")
        else:
            log("communication with 01 ended")

    def quit(self):
        """Close VCDS altogether, from the unit selection back to Konec."""
        if self.exists(T_SELECT):
            self.click("select", self.win(T_SELECT), 1249)
            time.sleep(1.5)
        self.click("main", self.win(T_MAIN), 1026)
        time.sleep(2)
        try:
            self.Application(backend="win32").connect(path=VCDS_EXE, timeout=1)
            log("WARNING: VCDS is still running")
        except Exception:
            log("VCDS closed")

    def dismiss_init(self):
        if self.exists(T_INIT):
            self.click("init", self.win(T_INIT), 2)
            log("the unit stopped answering; OK pressed")
            time.sleep(3)
            return True
        return False


def part_path(out, n):
    if n == 1:
        return out
    root, ext = os.path.splitext(out)
    return "%s-%d%s" % (root, n, ext)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--faults", metavar="TXT",
                   help="only read the engine's fault memory into TXT and print it; no logging")
    p.add_argument("--groups", nargs="+", help="up to three, e.g. 014 001 003")
    p.add_argument("--out", help="the CSV VCDS writes; parts get -2, -3 ...")
    p.add_argument("--stop", help="create this file to stop (default: OUT.stop)")
    p.add_argument("--seconds", type=float, help="stop after this long")
    p.add_argument("--keep-open", action="store_true",
                   help="leave VCDS and the communication with 01 open at the end")
    a = p.parse_args(argv)
    if a.faults:
        v = Vcds()
        try:
            lines = v.read_faults()
        finally:
            v.end_session()
            if not a.keep_open:
                v.quit()
        text = "%s  01-Motor, fault memory (read by vcds_log.py)\n%s\n" % (
            time.strftime("%Y-%m-%d %H:%M:%S"), "\n".join(lines))
        with open(a.faults, "w", encoding="utf-8") as f:
            f.write(text)
        print(text, end="")
        log("DONE")
        return 0
    if not a.groups or not a.out:
        p.error("--groups and --out are needed to log")
    if len(a.groups) > 3:
        p.error("VCDS shows three groups at a time")
    stop = a.stop or a.out + ".stop"
    t0 = time.time()

    v = Vcds()
    n = 1

    def stopping():
        return os.path.exists(stop) or (a.seconds and time.time() - t0 > a.seconds)

    # Everything from here on is inside the try, so that however it ends --
    # the stop file, an error, Ctrl-C -- the log dialog is stopped and
    # closed, which is what writes the file. A log left running is the one
    # outcome this tool must never have.
    try:
        blocks = v.open_blocks(a.groups)
        v.start_log(blocks, part_path(a.out, n))
        t0 = time.time()            # --seconds counts logging, not setup
        while not stopping():
            if v.dismiss_init():
                n += 1
                while not stopping():
                    try:
                        blocks = v.open_blocks(a.groups)
                        v.start_log(blocks, part_path(a.out, n))
                        break
                    except Exception as e:      # the ECU still asleep: wait, retry
                        log("reconnect failed (%s); retrying" % str(e)[:80])
                        v.dismiss_init()
                        time.sleep(3)
            time.sleep(0.5)
        log("stopping")
    finally:
        for attempt in range(3):
            try:
                v.stop_log()
                break
            except Exception as e:
                log("closing the log failed (%s); again" % str(e)[:80])
                time.sleep(2)
        if v.log_dialog() is not None:
            log("WARNING: the log dialog is still open -- close it in VCDS")
        else:
            log("log closed; %d part(s)" % n)
            if a.keep_open:
                log("communication left open (--keep-open)")
            else:
                try:
                    v.end_session()
                    v.quit()
                except Exception as e:
                    log("WARNING: ending the communication or VCDS failed (%s)" % str(e)[:80])
        log("DONE")
        if os.path.exists(stop):
            os.remove(stop)
    return 0


if __name__ == "__main__":
    sys.exit(main())
