# ONE GO AI SERVER


### Installation
`pip install -r requirements.txt`

#### cf) konlpy installation

**Windows**
1. install JDK(1.7+ version)
2. set PATH of JDK(JAVA_HOME)
3. [install Jpype](https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype)(JPype1‑1.1.2‑cp3x‑cp3x‑win_amd64.whl)  
  python 3.8x -> Jpype cp38
  
**other OS**

&emsp;https://konlpy-ko.readthedocs.io/ko/v0.4.3/install/

### Scripts

#### `python start_flask.py`
Runs the app.
Open http://localhost:5000 to view it in the browser.

<br>
<br>


## FLASK REST API

### __1. Sentence Complete__
`complete.py`

How to run? python complete.py in path 'libs/sentence_complete'
<br>

What is input & output?
  |input|output|
  |--|--|
  |Key, Value|list in json|
<br>
  
How to check on POST MAN? 
  <li> POST http://localhost:2727/complete
  <li> Body > form-data > KEY text, VALUE "the sentence what you want to complete"
    
  ![image](https://user-images.githubusercontent.com/76719920/129465341-f50930f0-75c2-453c-92a4-62daaae60cd5.png)

