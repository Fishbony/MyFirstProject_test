# OCR of PTA(Pure Tone Audiometry) pdf file

> Update  2020.03.20
>
> Update PTA_transfer.py

## Background

In our hospital, PTA results were get in pdf format.

People need to input the result in different frequency by hand so this project is used to free our hand. Tesseract were chosen as OCR engine in our project. Available at https://github.com/tesseract-ocr/tesseract. 

This project does not include a GUI application.

## TODO

* complete rename function
* input the locations of different frequency easily and save them to isolated file.

## File list

```
./test
./pics
./README.md
./PTA_rename.py (incomplete)
./PTA_transfer.py
./OCR.py
```

## How to run file

Windows platform

* File prepare. Ready to OCR

  * Rename your PTA pdf files. It could rename your file by OCR. This function is incomplete. DO NOT run this file. If you have renamed your pdf files, this step could be skipped.

    ```cmd
    python PTA_rename.py
    ```

    

  * Transfer your pdf to jpg.

    ```cmd
    python PTA_transfer.py
    ```

    

* OCR

  * OCR your images and get a csv file.

    ```cmd
    python OCR.py
    ```

## Support

* Python 3.6.7
* tesseract 5.0.0
* Poppler: Available at https://poppler.freedesktop.org/ 

## Authors & Contributors List

Name: Fishbony

Affiliates: Postgraduate student in Shantou University Medical College and resident in Guangdong Provincial Peoples' Hospital

Email: czhangent@163.com
