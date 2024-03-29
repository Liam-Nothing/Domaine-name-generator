```
==================================================
OVH add a challenge to block the scraping.
The program is no longer functional.
==================================================
```

# Domaine name generator with OVH

<p align="center">
    <img src="README_SRC/main_img.png" width="500">
</p>

- ## Description :
  
  This program is designed to find interesting domains from a text list. The program uses Ovh to determine whether a domain is available or not. It utilizes async functions and data scraping with chromedriver.exe.

- ## Requirements :
  
  - Python 3
  - Chrome

- ## Install :
  
  - Install `requirements.txt` : `pip install -r requirements.txt`

- ## How to use :

  - Fill prefix of words list in `_prefix.txt`
  - Fill word list in `_words.txt`
  - Fill top-level domain in `_top_level_domains.txt`
  - Run `python domain_name_generator_and_tester.py _prefix.txt _words.txt _top_level_domains.txt`

- ## Troubleshooting :

  - If you have this error :
    ```
      ====== WebDriver manager ======
      Current google-chrome version is 116.0.5845
      Get LATEST chromedriver version for 116.0.5845 google-chrome
      Traceback (most recent call last):
        File "X:\XXX\domain_name_generator_and_tester.py", line 48, in <module>
    ```
    - `pip install --upgrade webdriver_manager`