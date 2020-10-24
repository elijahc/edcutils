# edcutils
My personal utils

## Datasets

### National Ambulatory Medical Care Survey

The National Ambulatory Medical Care Surveys (NAMCS) supplydata on ambulatory medical care provided in physicians' offices. The2006 survey contains information from 29,392 patient visits to 1,455physicians' offices. Data are available on the patient's smokinghabits, reason for the visit, expected source of payment, thephysician's diagnosis, and the kinds of diagnostic and therapeuticservices rendered. Other variables cover drugs/medications ordered,administered, or provided during office visits, with information onmedication code, generic name and code, brand name, entry status,prescription status, federal controlled substance status, compositionstatus, and related ingredient codes. Information is also included onthe physician's specialization and geographic location. Demographicinformation on patients, such as age, sex, race, and ethnicity, wasalso collected. In addition, the 2006 survey contains two new sampling strata which are from 104 Community Health Centers (CHCs) and 200 oncologists.

See [Cookbook](https://www.icpsr.umich.edu/SDA/NACDA/28403-0001/CODEBOOK/NMCS.htm) here for data dictionary and data management plan

#### Usage


```python
from edcutils.datasets import namcs

private_practice = namcs.load_data(year=[2013,2014])
```
> Downloading data from ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/namcs/spss/namcs2013-spss.zip