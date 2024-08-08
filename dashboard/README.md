# Requirements
- make it easier to maintain the botanical garden
- monitor the health of the plants in the conservatory and alert the gardeners when there is a problem.

* [x] To be able to view the data in real-time
* [x] To be able to view the data from the long-term storage
* [x] View graphs of the latest temperature and moisture readings for every plant
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
See [https://excalidraw.com/#json=C3RxBSzgMNaBPaRIav5q2,aHKyiquHU67wbIa11_X9xg]
<br>Have two tabs, one for live data one for historical (live one by default/ what you see first)
<br>Filters on a sidebar - Same exact filters for both for now
<br>Colours - green shades to match plant vibes
<br>Above and Beyond: Incorporate pictures with the plant data

### Live tab
- Display warnings first
- Temperature vs Moisture

### Historical tab
- <span style="color:red">Moisture</span> and Temperature vs time per plant - depends on filters
- (Above and beyond? Add graph for warnings by plant in the history tab)


## Other info
Warnings to consider: what is a bad soil moisture, temperature, missing water?
- Temperature: 20 at night, 25-30°C during the day
- Soil: 20% - 40%
- Water: twice a week in the summer, 1–2 weeks in winter

Temperature:
During hours of light, stick to a temperature between 25°C-30°C, depending on your lamp's light output. During dark hours you can drop this to around 20°C.
https://plagron.com/en/grow-topics/temperature#:~:text=During%20hours%20of%20light%2C%20stick,day%20as%20small%20as%20possible.

Soil Moisture:
The majority of flowers, trees, and shrubs require moisture levels between 21% - 40%
https://www.acurite.com/blog/soil-moisture-guide-for-plants-and-vegetables.html#:~:text=It%20is%20important%20to%20note,between%2041%25%20%2D%2080%25.

Tropical plants might need water twice a week in the summer, 1–2 weeks in winter https://www.thesill.com/blog/drink-up
In general, houseplants' potting soil should be kept moist, but not wet. They normally need watering once or twice a week in the spring and summer, but less in the autumn and winter. https://www.gardenhealth.com/advice/houseplant-care/how-to-water-and-feed-houseplants#:~:text=In%20general%2C%20houseplants'%20potting%20soil,is%20not%20always%20the%20case.
