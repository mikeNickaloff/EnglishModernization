# EnglishModernization

**The ultimate modernization for the English language.**  
This project makes it possible to read English *without* getting a headache every time you hit a silent letter, a random vowel shift, or a word imported from 1400s French for no reason.

Instead of fighting with traditional spelling, this repo gives you:

- A **modern phonetic spelling** for the words people actually use today.
- A **converter script** that takes “ancient” English spelling and produces a consistent, readable phonetic form.

---

## What this project does

Traditional English spelling is:

- Inconsistent  
- Full of silent letters  
- Packed with one-off exceptions  
- A nightmare for learners, TTS engines, and frankly, most normal people  

This project replaces that mess with a **simplified phonetic spelling system**, mapping each common word into a form that:

- Looks like it sounds  
- Uses consistent patterns  
- Is easy to read and pronounce  
- Works well for text-to-speech or learning

In short: it turns:

> “you know what this does – better than anything – makes English actually readable.”

into something like:

> `yu no wut thees duz – betur than enithing – mayks inglish akshli ridubl.`

Same language, less suffering.

---

## Repository contents

- `american.txt`  
  A dictionary mapping standard English vocabulary to a modernized phonetic spelling.  
  Each line is typically in the form:

  ```text
  word phonetic_form
  ```
 - `modernize.py`
A script that reads normal English text from stdin or arguments, looks up each word in american.txt, and outputs the modern phonetic version.

Depending on how you wire it, it can:

- Normalize case

- Handle punctuation

- Fall back gracefully when a word is missing from the dictionary

Usage
1. Basic command-line conversion

From the repo directory:

```
echo "you know what this does - better than anything - makes english actually readable." \
|  python3 modernize.py --dict american.txt
```


Example output:

`yu no wut thees duz - betur than enithing - mayks inglish akshuli reedabl.`



2. Converting a text file
```
python3 modernize.py --dict american.txt < input.txt > output_phonetic.txt
```


Now output_phonetic.txt contains the modernized phonetic spelling of your original text.


## Rule-based normalization (optional)
If extended with rule files, the system can apply regex-style transformations to smooth out irregularities and unify patterns (e.g. ough, eigh, tion, etc).

### Token-by-token conversion
modernize.py processes the input text word by word, replacing each term with its phonetic counterpart where available.

## What this is good for

- Making English text more readable for learners

- Creating phonetic subtitles or captions

- Feeding simplified text to TTS systems

- Experimenting with orthography reform without inventing a whole new alphabet

- Just… not staring at “through, tough, though, thought, bough” and questioning reality


---------------

# englishmodernizashun

**Thu ultumut madurnizayshu fur thu Inglish langwuj.**  
Thees prajekt mayks it pasubul tu rt Inglish *withowt* jeting ay hedayk evuri teem yu heet ay silunt letur, ay randum vowul shift, ur ay wurd importid frum 1400es French fur no rizun.

Inst uv fiting with trudishunul speling, thees ripo jivz yu:

- AY **madurn fonetic speling** fur thu wurdz pipul akshuli yus tuday.
- AY **kunvurtur skript** that tayks “aynshunt” Inglish speling and prudusuz ay kunsistunt, reedabl fonetic form.

---

## Wut thees prajekt duz

Trudishunul Inglish speling iz:

- Inkunsistunt  
- Ful uv silunt leturz  
- Pakt with wun-of iksepshunz  
- AY nitmer fur leerners, TS enjunz, and frangkli, mos normul pipul  

Thees prajekt riplaysiz that mz with ay **simplufid fonetic speling sistum**, maping ich kamun wurd intu ay form that:

- Luks lik it sownz  
- Yusuz kunsistunt paturnz  
- Iz izi tu rt and prunowns  
- Wurks wel fur tekst-tu-spich ur lurning

In short: it turnz:

> “yu no wut thees duz – betur than enithing – mayks Inglish akshuli reedabl.”

intu sumthing lik:

> `yu no wut thees duz – betur than enithing – mayks inglish akshli ridubl.`

Saym langwuj, lz sufuring.

---

## Ripazutori kantents

- `umerukun.tkst`  
  AY dikshuneri maping standurd Inglish vokabyuleri tu ay modernizt fonetic speling.  
  Ich leen iz tipikli in thu form:

  ```tekst
  wurd fonetic_form
  ```
 - `madurniz.py`
AY skript that ridz normul Inglish tekst frum stdeen ur arjyumunts, luks up ich wurd in umerukun.tkst, and outputs thu madurn fonetic vurzhun.

Dipending an how yu wiur it, it kan:

- Normaliz kays

- Handul pungkuayshun

- Fal bak graysfuli wen ay wurd iz mising frum thu dikshuneri

Yusuj
1. Baysik kumand-leen kunvurzhun

Frum thu ripo direkturi:

```
eko "yu no wut thees duz - betur than enithing - mayks inglish akshuli reedabl." \
|  pithan3 madurniz.py --dict umerukun.tkst
```


Igzampul owtput:

`yu no wut thees duz - betur than enithing - mayks inglish akshuli reedabl.`



2. Kunvurting ay tekst feel
```
pithan3 madurniz.py --dict umerukun.tkst < input.tkst > owtput_fonetic.tkst
```


Now owtput_fonetic.tkst kuntaynz thu modernizt fonetic speling uv yor urijunul tekst.


## Rul-bayst normalizashun (apshunul)
If ikstendud with rul filz, thu sistum kan upli rejeks-steel transfurmayshunz tu smuth owt eerejyulerutiz and yunufi paturnz (i.ji. ou, ay, shun, etseturu).

### Tokun-bi-tokun kunvurzhun
madurniz.py prasesuz thu input tekst wurd bi wurd, riplaysing ich turm with its fonetic kownturpart wer uvaylubul.

## Wut thees iz gud fur

- Mayking Inglish tekst mor reedabl fur leerners

- Kriayting fonetic subtitulz ur kapshunz

- Fiding simplufid tekst tu TS sistumz

- Eksperumenting with orthografy ruform withowt inventing ay hol nu alfubet

- Just… nat stering at “thru, tuf, tho, thot, bow” and kweskuning rialuti

