# Gaussian Distribution Notes
-Date: 10-12-2020

## Sources:
- 1) https://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
- 2) https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.ndimage.filters.gaussian_filter1d.html
- 3) https://www.youtube.com/watch?v=qo-zZzP3Yx0

## Notes:
- Paper's Note: we first smooth eachcoordinate of the normalized pose vector, along the time di-mension, with a 5 by 1 Gaussian filter (σ=1). Note thatGaussian smoothing produces a lag of two frames.

- (Mehmet) Based on what the paper said, I believe they are using a 1D GD as its a 5 by 1 instead of a 5 by 5.

- GD is used to remove detail and noise within a data set.


- Gaussian Distribution (1D):
p(x) = 1/root(2*pi*o) * e^(-(x-u)^2/(2*o)^2)
or
*If u = 0 and o^2 =1...
p(x) = 1/root(2*pi) * e^-(x^2/2)



