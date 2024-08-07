# Requirements
- make it easier to maintain the botanical garden
- monitor the health of the plants in the conservatory and alert the gardeners when there is a problem.

* [*] To be able to view the data in real-time
* [*] To be able to view the data from the long-term storage
* [*] View graphs of the latest temperature and moisture readings for every plant
<br>'latest', I assume means latest minute, so this would be updating every minute if you refresh (however, should not be noticeable as the readings change minimally)

# Ideas of what to include:

## Filters and why:
Main:
- <u>**Filter by**</u> Plant id - makes it easier to look at any specific plant - say if you find a warning with a plant, it is easy to look for said plant
- <u>**Filter by**</u> Recorded time - have this as a slider to maybe only see data from today or only from last week etc
- <s><u>**Filter by**</u> Plant scientific name - potentially you may only want to look at a species at a time</s> 
<br> As for now each name is different, it would be a little useless in our case however, this would be useful in a real-world case.

Dropdown - <u>**Filter by**</u>:
- Botanist (name)- potentially some may be better than others so you may want to group by to see for example who is most suited to assign a plant to that comes from France
- Origin Continent - potentially to see if a warning is affecting a group of plants from the same area or for example to gather information about the ideal temperature for the plants from that area. [Maybe latitude (combined with like a longitude range) may provide more insight but for now it's beyond our scope]

## Graphs
### Live
- [Scatter Plot] Current Temperature vs Current Moisture - will have one point per plant and will have lines to show the expected values and thus if the plant's values are in the expected range. Clear visual of which plants to look our for and which are ok. (Note, the plant ID will be displayed when hovering over a point)

### Historical
- [Line Graph] For each plant. This graph has two y-axes, one with temperature, one with moisture (when watered will be seen by spikes in moisture) and time will be the x axis.

## Layout
Have two tabs, one for live data one for historical (live one by default/ what you see first)
Filters on a sidebar - Same exact filters for both for now
Colours - green shades to match plant vibes
Above and Beyond: Incorporate pictures with the plant data

### Live tab
- Display warnings first
- Temperature vs Moisture

### Historical tab
- Just an idea idk if it's good:
<br>Have this like a table (in terms of structure - not have an actual table - do this but putting things in containers) so maybe:

(Filter sidebar over here)|Plant (scientific name)|Historical Temperature|Historical Moisture|When Watered|
---|----|----|----|----|
---|Heliconia schiedeana| graph | graph | graph |
---|Cordyline fruticosa| graph | graph | graph |



###### Other info
What are warnings:
- what is a bad soil moisture, temperature, missing water?

Comments from Chris
- do as much as you can in sql not in pandas
- if things go wrong - you gauge this but keep in mind some erroneous values are only momentarily
- add point in readme about what happens if there are 1000 plants and if there are 200000000 plants and suggest a potential solution or mention something like (currently there is no scaling but there could be)


IMPROVE
+ add graph for warnings by plant in the history tab




