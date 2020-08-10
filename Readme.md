### Graphlet-Based Time Series Plots Using Seaborn/Matplotlib

This repository contains object-based code for creating "graphlet" based time series plots. These allow stacking multiple categorical and continuous variables into a single "dashboard" style plot visualizing interactions among variables. The example plot illustrates four types of graphlets based on sample data:
* Categories - Categorical data in a single y-columns
* Multiple Flag Columns - Event "flags" such as (1/0) or (yes/no) in multiple y-columns
* Continuous y variable plotted without rescaling its values
* A rescaled continuous y-variable with specified tick labels in alternate units than the underlying y-axis

<p style="text-align: center;"> Example time-series data
<br/><br/><img src=Assets/Sample_Data.png alt="Sample Data" width=250></p>

<p style="text-align: center;"> <img src=Assets/Plot_example.png alt="Example Graphlet-based Plot" width=800><br/></p>


#### Code Details
The graphlet code is in the Python library file, libs/graphlet_plots.py and is based on Seaborn and Matplotlib. The *.py code is also pasted into initial cells of graphlet.ipynb for ease of debugging. The Jupyter notebook generates the example graphic above. The code takes care of translating original data columns into y-axis units that grounded by the first, continuous y-variable and its 0 to 100 range. The code uses Python dictionaries to gather needed parameters for each graphlet including its y-axis anchor point, dot color and size, scaling factors and ticklabel dictionary. For categorical and flag variables, y-axis translation takes the form of generating spaced y-values from the original categories. For continuous variables, it can save effort to use one continuous, y-variable as the unscaled basis for the plot and to specify scaling factors for other continuous y-variables to translate them into this basis --with appropriate tick labels specified to label in the variable's original units. The 0 - 18 hrs tick labels are an example of this.

#### Business, R&D and Manufacturing Data Applications
Graphlet plots are great for visualizing business and technical data and condense information more naturally than subplots in many cases. An example is showing sales trends as continuous variables while using flags to highlight the onset of marketing events such as promotions, coupons and advertising. A second example is highlighting numerous flag events related to a manufacturing process --in concert with continuous variables such as temperatures, pressures and load cell amounts. A third example is visualizing consumer research such as a diary study where product wear time and consumer rating of the experience are continuous variables and various product failure modes or usage experiences are flag variables (Used hot water/cold water, Diaper leaked/didn't leak and so on) Plotting these multiple inputs in a graphlet-based dashboard is a way to bring out macroscopic trends such as consumers accommodating to the product and getting improved usage experiences over time.

There are numerous, public examples of this type of information-rich plot. [Stockcharts.com](https://stockcharts.com/h-sc/ui?s=aapl) is a particularly inspirational example. Their charts have numerous technical analysis and stock fundamentals endpoints represented in an engaging "graphlet" plot that also makes intricate use of colors and shading to bring out additional endpoints in stock trends.

#### *Version/Upgrade notes*
8/10/20 - J.D. Landgrebe - Initial Github post of generic code that was basis for a consulting client project
