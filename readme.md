\# SpookyAppX (test app)



This is a tiny cross-platform test app used to verify installer/payload behaviour.

It writes a log to the user's home directory and (if available) shows a simple GUI.



Run:

&nbsp;- GUI: `python spookyappx.py`

&nbsp;- Headless: `python spookyappx.py --headless`

&nbsp;- Log only: `python spookyappx.py --log-only`



Log location: `~/spookyappx.log` or `%USERPROFILE%\\spookyappx.log`



Test advice:

&nbsp;- Test manually on your target OS or inside a VM before using an automated HID installer.

&nbsp;- On machines without Tkinter, use `--headless`.



