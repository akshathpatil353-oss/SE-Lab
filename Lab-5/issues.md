# Lab 5: Static Code Analysis — Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command execution | Security — High | 60 | `os.system()` executes a shell command using the supplied filename, which may allow command injection. | Remove shell execution and print the export message directly. |
| Weak MD5 hash | Security — High | 49 | MD5 is a weak hashing algorithm and should not be used for security-sensitive purposes. | Replace MD5 with SHA-256. |
| Use of eval | Security — Medium | 44 | `eval()` evaluates an expression string and can execute unsafe code. | Replace `eval()` with safe GPA calculation logic. |
| Bare exception handler | Bug / Code Quality | 26 | A bare `except` catches errors without identifying their cause and silently ignores them. | Catch the expected exception types and handle invalid student IDs. |
| Insecure random PIN generation | Security — Low | 53 | `random.randint()` is not suitable for generating security-sensitive PINs. | Use the `secrets` module. |
| Hardcoded portal token | Security — Low | 64 | A token is embedded directly in the source code and printed to the terminal. | Read the token from an environment variable and avoid printing its value. |
| Mutable default argument | Bug / Code Quality | 15 | The default list `grade_list=[]` is shared across function calls. | Use `None` as the default and initialize the list inside the function. |
| Unused variables and import | Code Quality | 6, 31, 43 | The `json` import, `grace_marks`, and `avg_score` are unused in the original implementation. | Remove unused code or use variables where required. |
| Naming and missing docstrings | Code Quality | 15, 23, 30, 41, 48, 52, 56, 63 | The function `addGrade` violates snake_case naming, and several functions lack docstrings. | Rename the function to `add_grade` and add concise docstrings. |
| Formatting violations | Style | 19, 34, 75 | Long lines and a missing final newline violate style checks. | Break long lines and add a final newline. |

Note: Line numbers refer to the original, unmodified source file and may change after fixes.