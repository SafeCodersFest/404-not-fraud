# Perfil de Dataset

## Inventario
- Motor_Vehicle_Collisions_Crashes.csv: 20000 filas, 29 columnas, 17816 KB
- fraud_oracle.csv: 15420 filas, 33 columnas, 21534 KB

## Motor_Vehicle_Collisions_Crashes.csv
### Columnas
| Columna | Tipo | % Faltantes | Únicos | ID? |
|---------|------|-------------|--------|-----|
| CRASH DATE | date | 0.0 | 403 | No |
| CRASH TIME | text | 0.0 | 1421 | No |
| BOROUGH | categorical | 34.63 | 5 | No |
| ZIP CODE | float | 34.64 | 187 | No |
| LATITUDE | float | 8.12 | 13033 | No |
| LONGITUDE | float | 8.12 | 11788 | No |
| LOCATION | text | 8.12 | 14339 | No |
| ON STREET NAME | text | 27.12 | 2493 | No |
| CROSS STREET NAME | text | 53.84 | 2637 | No |
| OFF STREET NAME | text | 72.88 | 5221 | No |
| NUMBER OF PERSONS INJURED | int | 0.0 | 11 | No |
| NUMBER OF PERSONS KILLED | int | 0.0 | 3 | No |
| NUMBER OF PEDESTRIANS INJURED | int | 0.0 | 4 | No |
| NUMBER OF PEDESTRIANS KILLED | int | 0.0 | 2 | No |
| NUMBER OF CYCLIST INJURED | int | 0.0 | 4 | No |
| NUMBER OF CYCLIST KILLED | int | 0.0 | 2 | No |
| NUMBER OF MOTORIST INJURED | int | 0.0 | 11 | No |
| NUMBER OF MOTORIST KILLED | int | 0.0 | 3 | No |
| CONTRIBUTING FACTOR VEHICLE 1 | text | 0.48 | 52 | No |
| CONTRIBUTING FACTOR VEHICLE 2 | categorical | 22.11 | 37 | No |
| CONTRIBUTING FACTOR VEHICLE 3 | categorical | 89.22 | 16 | No |
| CONTRIBUTING FACTOR VEHICLE 4 | categorical | 97.13 | 6 | No |
| CONTRIBUTING FACTOR VEHICLE 5 | categorical | 99.18 | 5 | No |
| COLLISION_ID | int | 0.0 | 20000 | Sí |
| VEHICLE TYPE CODE 1 | text | 1.12 | 134 | No |
| VEHICLE TYPE CODE 2 | text | 32.73 | 153 | No |
| VEHICLE TYPE CODE 3 | categorical | 89.96 | 30 | No |
| VEHICLE TYPE CODE 4 | categorical | 97.3 | 17 | No |
| VEHICLE TYPE CODE 5 | categorical | 99.22 | 8 | No |

Duplicados: 0

### Muestra (primeras 5 filas)
| CRASH DATE | CRASH TIME | BOROUGH | ZIP CODE | LATITUDE | LONGITUDE | LOCATION | ON STREET NAME | CROSS STREET NAME | OFF STREET NAME | NUMBER OF PERSONS INJURED | NUMBER OF PERSONS KILLED | NUMBER OF PEDESTRIANS INJURED | NUMBER OF PEDESTRIANS KILLED | NUMBER OF CYCLIST INJURED | NUMBER OF CYCLIST KILLED | NUMBER OF MOTORIST INJURED | NUMBER OF MOTORIST KILLED | CONTRIBUTING FACTOR VEHICLE 1 | CONTRIBUTING FACTOR VEHICLE 2 | CONTRIBUTING FACTOR VEHICLE 3 | CONTRIBUTING FACTOR VEHICLE 4 | CONTRIBUTING FACTOR VEHICLE 5 | COLLISION_ID | VEHICLE TYPE CODE 1 | VEHICLE TYPE CODE 2 | VEHICLE TYPE CODE 3 | VEHICLE TYPE CODE 4 | VEHICLE TYPE CODE 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 09/11/2021 | 2:39 | nan | nan | nan | nan | nan | WHITESTONE EXPRESSWAY | 20 AVENUE | nan | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Aggressive Driving/Road Rage | Unspecified | nan | nan | nan | 4455765 | Sedan | Sedan | nan | nan | nan |
| 03/26/2022 | 11:45 | nan | nan | nan | nan | nan | QUEENSBORO BRIDGE UPPER | nan | nan | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Pavement Slippery | nan | nan | nan | nan | 4513547 | Sedan | nan | nan | nan | nan |
| 11/01/2023 | 1:29 | BROOKLYN | 11230.0 | 40.62179 | -73.970024 | (40.62179, -73.970024) | OCEAN PARKWAY | AVENUE K | nan | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Unspecified | Unspecified | Unspecified | nan | nan | 4675373 | Moped | Sedan | Sedan | nan | nan |
| 06/29/2022 | 6:55 | nan | nan | nan | nan | nan | THROGS NECK BRIDGE | nan | nan | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Following Too Closely | Unspecified | nan | nan | nan | 4541903 | Sedan | Pick-up Truck | nan | nan | nan |
| 09/21/2022 | 13:21 | nan | nan | nan | nan | nan | BROOKLYN BRIDGE | nan | nan | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Passing Too Closely | Unspecified | nan | nan | nan | 4566131 | Station Wagon/Sport Utility Vehicle | nan | nan | nan | nan |

## fraud_oracle.csv
### Columnas
| Columna | Tipo | % Faltantes | Únicos | ID? |
|---------|------|-------------|--------|-----|
| Month | categorical | 0.0 | 12 | No |
| WeekOfMonth | int | 0.0 | 5 | No |
| DayOfWeek | categorical | 0.0 | 7 | No |
| Make | categorical | 0.0 | 19 | No |
| AccidentArea | categorical | 0.0 | 2 | No |
| DayOfWeekClaimed | categorical | 0.0 | 8 | No |
| MonthClaimed | categorical | 0.0 | 13 | No |
| WeekOfMonthClaimed | int | 0.0 | 5 | No |
| Sex | categorical | 0.0 | 2 | No |
| MaritalStatus | categorical | 0.0 | 4 | No |
| Age | int | 0.0 | 66 | No |
| Fault | categorical | 0.0 | 2 | No |
| PolicyType | categorical | 0.0 | 9 | No |
| VehicleCategory | categorical | 0.0 | 3 | No |
| VehiclePrice | categorical | 0.0 | 6 | No |
| FraudFound_P | int | 0.0 | 2 | No |
| PolicyNumber | int | 0.0 | 15420 | Sí |
| RepNumber | int | 0.0 | 16 | No |
| Deductible | int | 0.0 | 4 | No |
| DriverRating | int | 0.0 | 4 | No |
| Days_Policy_Accident | categorical | 0.0 | 5 | No |
| Days_Policy_Claim | categorical | 0.0 | 4 | No |
| PastNumberOfClaims | categorical | 0.0 | 4 | No |
| AgeOfVehicle | categorical | 0.0 | 8 | No |
| AgeOfPolicyHolder | categorical | 0.0 | 9 | No |
| PoliceReportFiled | categorical | 0.0 | 2 | No |
| WitnessPresent | categorical | 0.0 | 2 | No |
| AgentType | categorical | 0.0 | 2 | No |
| NumberOfSuppliments | categorical | 0.0 | 4 | No |
| AddressChange_Claim | categorical | 0.0 | 5 | No |
| NumberOfCars | categorical | 0.0 | 5 | No |
| Year | int | 0.0 | 3 | No |
| BasePolicy | categorical | 0.0 | 3 | No |

Duplicados: 0

### Muestra (primeras 5 filas)
| Month | WeekOfMonth | DayOfWeek | Make | AccidentArea | DayOfWeekClaimed | MonthClaimed | WeekOfMonthClaimed | Sex | MaritalStatus | Age | Fault | PolicyType | VehicleCategory | VehiclePrice | FraudFound_P | PolicyNumber | RepNumber | Deductible | DriverRating | Days_Policy_Accident | Days_Policy_Claim | PastNumberOfClaims | AgeOfVehicle | AgeOfPolicyHolder | PoliceReportFiled | WitnessPresent | AgentType | NumberOfSuppliments | AddressChange_Claim | NumberOfCars | Year | BasePolicy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dec | 5 | Wednesday | Honda | Urban | Tuesday | Jan | 1 | Female | Single | 21 | Policy Holder | Sport - Liability | Sport | more than 69000 | 0 | 1 | 12 | 300 | 1 | more than 30 | more than 30 | none | 3 years | 26 to 30 | No | No | External | none | 1 year | 3 to 4 | 1994 | Liability |
| Jan | 3 | Wednesday | Honda | Urban | Monday | Jan | 4 | Male | Single | 34 | Policy Holder | Sport - Collision | Sport | more than 69000 | 0 | 2 | 15 | 400 | 4 | more than 30 | more than 30 | none | 6 years | 31 to 35 | Yes | No | External | none | no change | 1 vehicle | 1994 | Collision |
| Oct | 5 | Friday | Honda | Urban | Thursday | Nov | 2 | Male | Married | 47 | Policy Holder | Sport - Collision | Sport | more than 69000 | 0 | 3 | 7 | 400 | 3 | more than 30 | more than 30 | 1 | 7 years | 41 to 50 | No | No | External | none | no change | 1 vehicle | 1994 | Collision |
| Jun | 2 | Saturday | Toyota | Rural | Friday | Jul | 1 | Male | Married | 65 | Third Party | Sedan - Liability | Sport | 20000 to 29000 | 0 | 4 | 4 | 400 | 2 | more than 30 | more than 30 | 1 | more than 7 | 51 to 65 | Yes | No | External | more than 5 | no change | 1 vehicle | 1994 | Liability |
| Jan | 5 | Monday | Honda | Urban | Tuesday | Feb | 2 | Female | Single | 27 | Third Party | Sport - Collision | Sport | more than 69000 | 0 | 5 | 3 | 400 | 1 | more than 30 | more than 30 | none | 5 years | 31 to 35 | No | No | External | none | no change | 1 vehicle | 1994 | Collision |
