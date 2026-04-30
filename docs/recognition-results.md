# Recognition experiments

## Conditions

I used `conditions.py` to generate EAN-13 labels at different brightness gains
and horizontal viewing angles. A pinhole projection approximates a flat label
rotating around its vertical axis. A test passes only if the decoder returns
the expected value with no extra readings.

| Parameter | Values |
| --- | --- |
| Brightness gain | 0.25, 0.5, 1.0, 1.5 |
| Viewing angle | -60, -30, 0, 30, 60 degrees |
| Initial labels | 5901234123457, 4006381333931, 0012345678905 |

## Results on generated labels

I used the same 60 images to compare the direct decoder with the retry logic.
Then I tried five more label values with the same transformations. The current
tests cover eight values and 160 images. These images helped me develop the
code; they are not an independent camera benchmark.

| Run | Exact reads | Data |
| --- | --- | --- |
| Direct decoder, before retries | 54/60 | [Baseline](../results/synthetic-conditions-baseline.csv) |
| Scale retries and candidate confirmation | 60/60 | [Current run](../results/synthetic-conditions.csv) |
| Five additional labels, same conditions | 100/100 | [Additional labels](../results/additional-labels.csv) |

The original run had five missed reads and one extra incorrect candidate.
A 2x retry recovered two missed reads; second-scale confirmation removed the
extra candidate. A 3x retry recovered the final three +60-degree failures.

Reproduce the current runs with the development dependencies installed:

```sh
python conditions.py
python conditions.py --labels 978020137962 501234567890 123456789012 871234567890 761234567890 --output results/additional-labels.csv
```

## Limits

Changing image brightness does not reproduce a measured lighting level.
These images also leave out glare, focus, exposure, motion blur, and sensor
noise. Requiring agreement at another scale can reject a real label, and a
matching result can still be wrong. The retries add processing time. Results
also depend on the image and decoder versions.

For the physical trials, I plan to fix the distance, measure the label angle,
record lighting, and save frames of labels with known values. I'll count
missed and incorrect reads and measure the Pi's frame rate.
