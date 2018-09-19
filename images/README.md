# Image Compression Methods

Tested the following filetypes:
- .jpg/.jpeg
- .png

Tested the following methods:

Results for jpeg files:

| name           | method | change %| duration (s) | initialSize (MB) | finalSize (MB) | 
|----------------|--------|--------|----------|-------------|-----------| 
| population.jpg | zip    | 0.147  | 0.062    | 1.489       | 1.271     | 
| pluto.jpg      | zip    | 0.067  | 0.152    | 3.454       | 3.221     | 
| the moon.jpg   | zip    | 0.01   | 0.008    | 0.103       | 0.102     | 
| largeA.jpg     | zip    | 0.008  | 0.124    | 2.552       | 2.531     | 
| death star.jpg | zip    | 0.001  | 0.033    | 0.662       | 0.662     | 
| wallpaper.jpg  | zip    | 0.0    | 0.021    | 0.409       | 0.409     | 
| largeB.jpg     | zip    | 0.0    | 0.168    | 4.247       | 4.247     | 
| dog.jpg        | zip    | -0.001 | 0.01     | 0.12        | 0.12      | 

# PNG compression results

| name                   | method  | change | duration | initialSize | finalSize | 
|------------------------|---------|--------|----------|-------------|-----------| 
| 8k5y7u8gdvj11.png      | optipng | 43.158 | 4.396    | 1.29        | 0.733     | 
| ewjq9yb.png            | optipng | 42.301 | 1.334    | 0.564       | 0.326     | 
| Kuuro - Possession.png | optipng | 38.116 | 10.103   | 4.113       | 2.545     | 
| yLJ9uSm.png            | optipng | 31.228 | 1.731    | 0.222       | 0.153     | 
| Sapporo, Hokkaido.png  | optipng | 30.819 | 0.478    | 0.046       | 0.032     | 
| Seoul.png              | optipng | 25.367 | 2.428    | 2.329       | 1.738     | 
| Black Sun.png          | optipng | 25.089 | 1.775    | 0.229       | 0.172     | 
| ZYPoFxd.png            | optipng | 22.432 | 4.26     | 0.831       | 0.645     | 
| GDP_PPP.png            | optipng | 20.702 | 1.372    | 0.109       | 0.086     | 
| NAFTA.png              | zip     | 18.333 | 0.006    | 0.029       | 0.023     | 
| Antarctica.png         | zip     | 17.485 | 0.004    | 0.023       | 0.019     | 
| Fallen Titan.png       | optipng | 16.652 | 9.719    | 2.68        | 2.234     | 
| Antarctica.png         | optipng | 13.65  | 0.713    | 0.023       | 0.02      | 
| Pluto.png              | optipng | 12.87  | 2.409    | 0.437       | 0.38      | 
| NAFTA.png              | optipng | 10.603 | 0.589    | 0.029       | 0.026     | 
| Sapporo, Hokkaido.png  | zip     | 9.641  | 0.005    | 0.046       | 0.042     | 
| Pluto.png              | zip     | 6.201  | 0.034    | 0.437       | 0.409     | 
| Fukuchiyama,_Kyoto.png | optipng | 5.569  | 0.412    | 0.039       | 0.037     | 
| yLJ9uSm.png            | zip     | 3.621  | 0.012    | 0.222       | 0.214     | 
| GDP_PPP.png            | zip     | 3.533  | 0.007    | 0.109       | 0.105     | 
| Fukuchiyama,_Kyoto.png | zip     | 3.483  | 0.009    | 0.039       | 0.038     | 
| 8k5y7u8gdvj11.png      | zip     | 2.267  | 0.057    | 1.29        | 1.26      | 
| Black Sun.png          | zip     | 1.349  | 0.013    | 0.229       | 0.226     | 
| ZufjBPk.png            | optipng | 0.964  | 3.985    | 3.524       | 3.49      | 
| tic_tac_toe.png        | zip     | 0.155  | 0.025    | 0.616       | 0.615     | 
| ZYPoFxd.png            | zip     | 0.082  | 0.037    | 0.831       | 0.831     | 
| Kuuro - Possession.png | zip     | 0.013  | 0.207    | 4.113       | 4.112     | 
| genetic_algorithms.png | zip     | 0.005  | 0.004    | 0.037       | 0.037     | 
| ZufjBPk.png            | zip     | 0.001  | 0.126    | 3.524       | 3.524     | 
| tic_tac_toe.png        | optipng | 0      | 2.305    | 0.616       | 0.616     | 
| geography.png          | optipng | 0      | 0.351    | 0.061       | 0.061     | 
| genetic_algorithms.png | optipng | 0      | 0.191    | 0.037       | 0.037     | 
| 28_hour_day.png        | optipng | 0      | 0.408    | 0.061       | 0.061     | 
| anti_mind_virus.png    | optipng | 0      | 0.05     | 0.006       | 0.006     | 
| Fallen Titan.png       | zip     | -0.023 | 0.086    | 2.68        | 2.681     | 
| Seoul.png              | zip     | -0.023 | 0.09     | 2.329       | 2.329     | 
| ewjq9yb.png            | zip     | -0.026 | 0.022    | 0.564       | 0.565     | 
| geography.png          | zip     | -0.207 | 0.01     | 0.061       | 0.061     | 
| 28_hour_day.png        | zip     | -0.216 | 0.005    | 0.061       | 0.061     | 
| anti_mind_virus.png    | zip     | -2.944 | 0.003    | 0.006       | 0.006     | 

# Using `-06` with optipng

| name                   | method  | score | change | duration | initialSize | finalSize | 
|------------------------|---------|-------|--------|----------|-------------|-----------| 
| 8k5y7u8gdvj11.png      | optipng | 0     | 43.158 | 22.476   | 1.29        | 0.733     | 
| ewjq9yb.png            | optipng | 0     | 42.301 | 10.645   | 0.564       | 0.326     | 
| Kuuro - Possession.png | optipng | 0     | 38.116 | 72.229   | 4.113       | 2.545     | 
| yLJ9uSm.png            | optipng | 0     | 31.29  | 10.422   | 0.222       | 0.152     | 
| Sapporo, Hokkaido.png  | optipng | 0     | 30.819 | 2.959    | 0.046       | 0.032     | 
| Seoul.png              | optipng | 0     | 27.608 | 23.299   | 2.329       | 1.686     | 
| Black Sun.png          | optipng | 0     | 25.089 | 9.956    | 0.229       | 0.172     | 
| ZYPoFxd.png            | optipng | 0     | 23.657 | 24.132   | 0.831       | 0.635     | 
| GDP_PPP.png            | optipng | 0     | 20.702 | 7.391    | 0.109       | 0.086     | 
| Fallen Titan.png       | optipng | 0     | 17.137 | 112.535  | 2.68        | 2.221     | 
| Antarctica.png         | optipng | 0     | 13.65  | 5.1      | 0.023       | 0.02      | 
| Pluto.png              | optipng | 0     | 12.87  | 16.713   | 0.437       | 0.38      | 
| NAFTA.png              | optipng | 0     | 10.603 | 4.749    | 0.029       | 0.026     | 
| Fukuchiyama,_Kyoto.png | optipng | 0     | 5.569  | 2.029    | 0.039       | 0.037     | 
| ZufjBPk.png            | optipng | 0     | 4.182  | 46.238   | 3.524       | 3.376     | 
| geography.png          | optipng | 0     | 0.123  | 1.408    | 0.061       | 0.061     | 
| anti_mind_virus.png    | optipng | 0     | 0      | 0.279    | 0.006       | 0.006     | 
| 28_hour_day.png        | optipng | 0     | 0      | 1.969    | 0.061       | 0.061     | 
| tic_tac_toe.png        | optipng | 0     | 0      | 12.67    | 0.616       | 0.616     | 
| genetic_algorithms.png | optipng | 0     | 0      | 1.106    | 0.037       | 0.037     | 

# Converting to jpg

| name                   | method  | score | change  | duration | initialSize | finalSize | 
|------------------------|---------|-------|---------|----------|-------------|-----------| 
| Kuuro - Possession.png | convert | 0     | 90.274  | 0.134    | 4.113       | 0.4       | 
| ewjq9yb.png            | convert | 0     | 89.378  | 0.021    | 0.564       | 0.06      | 
| ZYPoFxd.png            | convert | 0     | 88.182  | 0.046    | 0.831       | 0.098     | 
| Fallen Titan.png       | convert | 0     | 88.104  | 0.123    | 2.68        | 0.319     | 
| Pluto.png              | convert | 0     | 85.273  | 0.067    | 0.437       | 0.064     | 
| Seoul.png              | convert | 0     | 84.611  | 0.056    | 2.329       | 0.358     | 
| ZufjBPk.png            | convert | 0     | 84.198  | 0.104    | 3.524       | 0.557     | 
| yLJ9uSm.png            | convert | 0     | 72.633  | 0.036    | 0.222       | 0.061     | 
| Fukuchiyama,_Kyoto.png | convert | 0     | 39.217  | 0.017    | 0.039       | 0.024     | 
| GDP_PPP.png            | convert | 0     | 33.458  | 0.036    | 0.109       | 0.072     | 
| 8k5y7u8gdvj11.png      | convert | 0     | 31.254  | 0.179    | 1.29        | 0.887     | 
| Sapporo, Hokkaido.png  | convert | 0     | 30.813  | 0.024    | 0.046       | 0.032     | 
| geography.png          | convert | 0     | 24.847  | 0.01     | 0.061       | 0.046     | 
| genetic_algorithms.png | convert | 0     | 16.999  | 0.009    | 0.037       | 0.031     | 
| tic_tac_toe.png        | convert | 0     | 15.17   | 0.05     | 0.616       | 0.523     | 
| NAFTA.png              | convert | 0     | 12.3    | 0.03     | 0.029       | 0.025     | 
| Black Sun.png          | convert | 0     | 5.119   | 0.085    | 0.229       | 0.218     | 
| Antarctica.png         | convert | 0     | -5.989  | 0.036    | 0.023       | 0.024     | 
| 28_hour_day.png        | convert | 0     | -50.358 | 0.014    | 0.061       | 0.091     | 
| anti_mind_virus.png    | convert | 0     | -70.814 | 0.007    | 0.006       | 0.01      | 



