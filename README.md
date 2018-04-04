# live-score-cli
Entertainment in your terminal.

## Getting Started

This is a very simple soccer live score crawler (www.livescores.com). You can clone and run it in terminal with python and also you can add custom arguments. It using beautifulsoup4 for parsing the page.

### Installing

Install the requirement package from requirements.txt.

```
pip install -r requirements.txt
```

## Running

You can simply run it like this.

```
python live_crawler.py
```

You can query the result with your preferred nationality, league, date and club like this.

```
python live_crawler.py --all
```

Add all argument to get all match for today. The rest example is to get the matches from preferred criteria.

```
python live_crawler.py --nation england
```

```
python live_crawler.py --league serie-a
```

```
python live_crawler.py --club juventus
```

```
python live_crawler.py --date 2017-09-19
``` 

You also can create sh file to run it.

Set tz cookies according you timezone.

## Authors

* **Yusuf Pradana Gautama** - [yusufgautama](https://github.com/yusufgautama)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## TODO

* Scrap all match for specified club, nation or league
* Add live standing
* ~~Scrap live and all match for specified date~~
