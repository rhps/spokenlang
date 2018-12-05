# [Spoken Language Identification Project](https://www.kaggle.com/toponowicz/spoken-language-identification)


### How to Guide:

* Extract Dataset from [Spoken Language Identification Project](https://www.kaggle.com/toponowicz/spoken-language-identification) to folder datasets/
* Build Docker Image, run the following command:
```bash
$ docker build -t rhps/spokenlang .
```
* Running Docker with the follwoing command:
```bash
$ docker run --rm -it -v $(pwd):/data rhps/spokenlang /data/en.mp3
```
with file to predict in data folder