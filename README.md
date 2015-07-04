# multiPrimerMatcher

Design to match sequences using multiple primers

### Method
Two sequencse files, ITS and 28S, shared two primers in the following way

PPP, QQQ, RRR, SSS are four different primers
File 1:
```
>I1
PPP*****QQQ*****RRR
```

File 2:
```
>R1
QQQ*****RRR*****SSS
```


If `QQQ****RRR` section in identical (100% match), them merged into
```
>I1_R1
PPP*****QQQ*****RRR*****SSS
```

### Usage

To run
```
python primer_matcher.py
```

parameters
* infile_its: file name for the ITS region
* infile_28s: file name for the 28S region
* outfile_name: output file name
* pattern: Regular expressing string

### TODO
* Better regular expression builder for the primer
* Everything is hard coded at moment, add some custom interface
