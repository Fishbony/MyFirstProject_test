# OCR of PTA(Pure Tone Audiometry) pdf file

> Update  2020.02.23

## Background

In our hospital, PTA results were get in pdf format.

People need to input the result in different frequency by hand so this project is used to free our hand. Tesseract were chosen as OCR engine in our project. Available at https://github.com/tesseract-ocr/tesseract. 

This project does not include a GUI application.

## TODO

* multithreading
* complete rename function
* input the locations of different frequency easily and save them to isolated file.

## File list

```
./test
./pics
./README.md
./PTA_rename.py (updated)
./PTA_transfer.py
./OCR.py
```

## How to run file

* File prepare. Ready to OCR

  * Firstly, please rename your PTA pdf files. If you have renamed your pdf files, this step could be skipped.

    ```cmd
    python PTA_rename.py
    ```

    

  * Secondly, please transfer your pdf to jpg. 

    ```cmd
    python PTA_transfer.py
    ```

    

* OCR

  * OCR your images and get a csv file.

    ```cmd
    python OCR.py
    ```

A table with csv format could be received.

## Support

* Python 3.6.7
* tesseract 5.0.0
* Poppler: Available at https://poppler.freedesktop.org/ 

## Authors & Contributors List

Name: Fishbony

Affiliates: Posgraduate student in Shantou University Medical College and resident in Guangdong Provincial Peoples' Hospital

Email: czhangent@163.com