
to run demo use this command:

python ./object_finder.py

Notes:

-thought about the problem some more, then realized something about template matching
-if the size of the image is m1 by n1 and the template has a size of m2 by n2. It will
	run in about P(m1 * n1 * m2 * n2). So if you scale all of them by a factor of k,
	you can change the runtime by ~k^4. So I just scaled everything down by a factor of
	2 and got it significantly faster. (4ms -> .6 ms)

