<b>Interactive Wiener-filter.</b><br>

Code used to apply wiener-filter to images present in a folder within `data`. To use, copy a folder containing `.tif` or `.tiff` images to use in the `data` folder, see `example_data`. A folder will be created in the `data` in which the Wiener filtered data will be stored, such as in `example_data_wiener`.
        
<b>Script developed by:</b><br>
<a href="https://www.rug.nl/staff/frank.mol/">Frank N. Mol</a> & 
<a href="https://www.rug.nl/staff/r.vlijm/">Rifka Vlijm</a> <br>
<a href="https://www.rug.nl/research/zernike/molecular-biophysics/">Molecular Biophysics</a> - 
<a href="https://www.rug.nl/research/zernike/molecular-biophysics/vlijm-group/">Vlijm Group</a><br>
<a href="https://www.rug.nl/research/zernike/">Zernike Institute of Advanced Materials</a><br>
<a href="https://www.rug.nl/">University of Groningen</a><br>

`wiener_filter.ipynb` is the notebook used for interactive wiener filter<br>
`wiener` is the package containing all used functions.<br>
`data` is the folder in which all data which needs to be analyzed must be stored. <br>
The images need to be of `.tiff` format, either 2D grayscale or 3D z-stack.<br>

The Wiener filter deconvolves an image by using the information on the Point-Spread-Funcunction (PSF) of the used Stimulated Emission Depletion (STED) and corresponding Confocal laser. Furthermore, the pixel size, noise-to-signal ratio and the signal influence ratio is needed (what ratio of the intensity is coming from STED and the corresponding confocal beam).