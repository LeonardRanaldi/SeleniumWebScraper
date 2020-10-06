<img src="https://raw.githubusercontent.com/leooJo/SeleniumWebScraper/master/identifier.png" title="identifier">


# Identifier -SeleniumWebScraper-
This is a Webcrawler based on Selenium frameworks for scrape web page of Twitter, Instagram and Facebook.

In the HYFINE-Framework folder you can find scripts able to extract fields such as name, genre, profile images of three of the most important Social Networks: Twitter, Facebook, Instagram.

For more information read the user manual of the framework in the HYFINE-Framework folder.


# HOW TO EXECUTE:

Is required an environment with the following requirements installed:
-Python >=3.5
-Selenium web-drivers

To scrape web page of Instagram, Facebook, Twitter should be executed the related script in the scraper folder.
Each script has a function that takes a link to a Facebook, Instagram or Twitter profile and returns a dictionary.

 Project Organization
------------

    |
    ├── /HYFINE-Framework                <- Folder containing HYFINE Framework      
    |       ├── USAGE                    <- Readme file that introduce Framework
    |       ├── buildDataset.py          <- Script for building dataset
    |       ├── build_final_dataset.py   <- Script for building dataset final dataset
    |       ├── correctURL.py            <- Script for check the integrity of url
    |       ├── writeAndReadFile.py      <- Script for write and read file created by buildDataset scripts
    |       ├── findInfoGenderAPI.py     <- Script for check information about profiles on twitter, instagram and Facebook
    |       ├── imageFace.py             <- Script for check face given an image (if it's present)
    |       ├── scrapeFacebook.py        <- Script for scrape scrape Facebook web page
    |       ├── scrapeTwitter.py         <- Script for scrape scrape Twitter web page
    |       └── scrapeInsta.py           <- Script for scrape scrape Instagram web page
    |
    ├── SVM_HYFINE.ipynb                 <- Implementation of HYFINE-classifier.
    ├── LICENSE                          <- License file
    └── README.md                        <- This Readme file
     
--------


# References:

http://docs.seleniumhq.org/


# SVM_HYFINE -Model-

This is the implementation of HYFINE-classifier on a pythonbook.

# Citation
If you use this code, please cite the paper:
```
@article{Ranaldi2020HidingYF,
  title={Hiding Your Face Is Not Enough: user identity linkage with image recognition},
  author={Leondardo Ranaldi and F. Zanzotto},
  journal={Social Network Analysis and Mining},
  year={2020},
  volume={10},
  pages={1-9}
}
```
```
