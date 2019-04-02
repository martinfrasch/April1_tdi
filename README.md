# bokeh on Heroku

[This](https://stackoverflow.com/questions/40558417/what-is-the-purpose-of-curdoc) is the most helpful concise explanation of how Bokeh works on a high level. I hope this is helpful to have it here. 

You can either run it locally with bokeh serve or on heroku (or any such service). If you choose to just run the script, you may choose to uncomment the output_file() and show(tabs) instead of curdoc.add_root, but you need the latter for it to work in bokeh server mode. Lastly, note that I import more bokeh widgets here than I end up using in this first release. These are left for future versions.
