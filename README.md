# Requirements
- make it easier to maintain the botanical garden
- monitor the health of the plants in the conservatory and alert the gardeners when there is a problem.

* [ ] To be able to view the data in real-time
* [ ] View graphs of the latest temperature and moisture readings for every plant
<br>^ <u>**by latest, means latest minute? So this would be updating every minute if you refresh? However, should not be noticeable as the readings change minimally**</u>
* [ ] To be able to view the data from the long-term storage

# Ideas of what to include:

## Filters and why:
Main:
- <u>**Filter by**</u> Plant id - makes it easier to look at any specific plant - say if you find a warning with a plant, it is easy to look for said plant
- <u>**Filter by**</u> Recorded time - potentially have this as a slider - to maybe only see data from today or only from last week etc
- <u>**Order by**</u> Last watered - not too sure about this one as it doesn't matter as some plants need to be watered more often than others
- <u>**Filter by**</u> Plant scientific name - potentially you may only want to look at a species at a time

Dropdown - <u>**Group by**</u>:
- Botanist (name)- potentially some may be better than others so you may want to group by to see for example who is most suited to assign a plant to that comes from France
- Origin Location - potentially to see if a warning is affecting a group of plants from the same area or for example to gather information about the ideal temperature for the plants from that area. [I feel like latitude (combined with like a longitude range) may provide more insight... but maybe not]
- Plant scientific name - potentially if you have multiple plants of the same species, you may only care about the type so not grouping may skew the data?

## Graphs
### Live
- Current temperature reading of every plant (I was thinking graph and expect this to be a quite up and down graph if we order by pant id, but could sort them in order of temperature so it looks better and you get a better idea of the various temperature range? <u>**Potentially ask stakeholders what they are looking to get out of this graph?**</u>)
<br>^ I was thinking of maybe having this instead of showing current temperature, show current temperature delta (compared to its average temperature)
- Exact same for moisture

### Historical
- for each plant, a graph for moisture, and temperature, and when watered
<br>(potentially combine moisture and temperature on the two sides of the graph and have two lines in the graph? but may get confusing)

## Layout
Have two tabs, one for live data one for historical (live one by default/ what you see first)
Filters on a sidebar - I would say have same exact filters for now for both
Colours? maybe green to match plant vibes
Above and Beyond: Incorporate pictures with the plant data

### Live tab
- Display warnings first
- Temperature vs plant id
- Moisture vs plant id

### Historical tab
- Just an idea idk if it's good:
<br>Have this like a table (in terms of structure - not have an actual table - do this but putting things in containers) so maybe:

(Filter sidebar over here)|Plant (scientific name)|Historical Temperature|Historical Moisture|When Watered|
---|----|----|----|----|
---|Heliconia schiedeana| graph | graph | graph |
---|Cordyline fruticosa| graph | graph | graph |



###### Other info
The key things they wanted to see were latest temperature and moisture reading for every plant so those go at the top.
- have two tabs one for live data and one for historical data

What are warnings:
- what is a bad soil moisture, temperature, missing water?

-do as much as you can in sql not in pandas
-if things go wrong - you gauge this but keep in mind some erroneous values are only momentarily
- add point in readme about what happens if there are 1000 plants and if there are 200000000 plants and suggest a potential solution or mention something like (currently there is no scaling but there could be)








