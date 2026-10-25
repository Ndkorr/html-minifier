# HTML Minifier 🥼

A python text-based processor script that **_minifies_**[^1] the input html file to reduce its file size by removing **whitespace** `' '`, **new lines** `'\n'`, **comments** `<!-- This is a comment -->` and such\
\
Inspired by **htmlnano**[^2] and **cssnano**[^3]
<br/>
<br/>
## Usage ⤵️
```
python htmlparser.py
```
> [!NOTE]
> _I know that the script is not a **parser**[^4] but my initial thought when creating it is for the script to understand html syntax but ended up just processing strings oh well. On the bright side, I would love to make this a complete parser later on._
<br/>

| Sample File       | Original Size | Using HTML Minifier | Comparison       |
| ---               | :---:         | :---:               | :---:            |
| myportfolio.html[^5]  | 73.2Kb        | 48.5Kb              | **~34% Saved**   |
| number-game.html[^6]  | 3.36Kb        | 2.39Kb              | **~29% Saved**   |

<br/>
<br/>
<br/>

## Requirements 🖋️
- [Python 3](https://www.python.org/downloads/) and above 
- Online Compilers/Debuggers[^7] (optional)
  > _if for some reason you don't want to install python on your device_
- **That's it!**

<br/>
<br/>
<br/>

## Function ▶️
I use the python [standard library](https://docs.python.org/3.11/library/index.html) primarily: `os` and `sys`
  > _**os** for file operations such as determining the .html extension, its file path and if it is a file. **sys** for destroying the runtime of the script_

<br/>

and [built-in function](https://docs.python.org/3.11/library/functions.html) `open()` for opening, reading and writing the file

<br/>

Aside from that no need to install third-party modules.

<br/>
<br/>

### That's all 

[^1]: [What is Minification](https://en.wikipedia.org/wiki/Minification_(programming))
[^2]: https://htmlnano.netlify.app/
[^3]: https://cssnano.github.io/cssnano/
[^4]: [What is parsing](https://www.geeksforgeeks.org/compiler-design/introduction-to-parsing/)
[^5]: [myportfolio.html](./myportfolio.html)
[^6]: [number-game.html](./number-game.html) a sample code from [mdn](https://developer.mozilla.org/) 
[^7]: https://www.onlinegdb.com/
