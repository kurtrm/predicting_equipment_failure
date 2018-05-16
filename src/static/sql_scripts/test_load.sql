CREATE TABLE IF NOT EXISTS testset
(
  id serial NOT NULL,
  VegMgmt SMALLINT,
  PMLate SMALLINT,
  WaterExposure SMALLINT,
  MultipleConnects SMALLINT,
  Storm SMALLINT,
  Age REAL,
  Manufacturer_GE SMALLINT,
  Manufacturer_Other SMALLINT,
  Manufacturer_Schneider_Electric SMALLINT,
  Manufacturer_Siemens SMALLINT,
  Repairs_Original SMALLINT,
  Repairs_Rebuild1 SMALLINT,
  Repairs_Rebuild2 SMALLINT,
  Repairs_Rebuild3 SMALLINT,
  AssetType_1_Phase_Pole_Transformer SMALLINT,
  AssetType_3_Phase_Transformer SMALLINT,
  AssetType_DFseries_Transformer SMALLINT,
  AssetType_Padmount_Transformer SMALLINT,
  AssetType_Voltage_Transformer SMALLINT,
  Status SMALLINT
);

COPY testset(VegMgmt,
             PMLate,
             WaterExposure,
             MultipleConnects,
             Storm,
             Age,
             Manufacturer_GE,
             Manufacturer_Other,
             Manufacturer_Schneider_Electric,
             Manufacturer_Siemens,
             Repairs_Original,
             Repairs_Rebuild1,
             Repairs_Rebuild2,
             Repairs_Rebuild3,
             AssetType_1_Phase_Pole_Transformer,
             AssetType_3_Phase_Transformer,
             AssetType_DFseries_Transformer,
             AssetType_Padmount_Transformer,
             AssetType_Voltage_Transformer,
             Status)
FROM '/mnt/c/Users/kurtrm/projects/predicting_equipment_failure/src/static/data/test_set.csv' DELIMITER ';' CSV;

CREATE TABLE IF NOT EXISTS latlong
(
  id serial NOT NULL,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  status SMALLINT
);

CREATE TABLE IF NOT EXISTS rocdata
(
  id serial NOT NULL,
  fpr DOUBLE PRECISION,
  lin DOUBLE PRECISION,
  thresh DOUBLE PRECISION,
  tpr DOUBLE PRECISION
);

COPY latlong(latitude, longitude, status)
FROM '/mnt/c/Users/kurtrm/projects/predicting_equipment_failure/src/static/data/lat_long.csv' CSV HEADER;

COPY rocdata(fpr, lin, thresh, tpr)
FROM '/mnt/c/Users/kurtrm/projects/predicting_equipment_failure/src/static/data/roc_data.csv' CSV HEADER;

CREATE TABLE IF NOT EXISTS threshold
(
  id serial NOT NULL,
  threshold REAL,
  cost INTEGER,
  revenue REAL,
  maintenance REAL,
  repair REAL
);

INSERT INTO threshold(threshold, cost, revenue, maintenance, repair)
VALUES
  (.3, 3500, 15.0, -25.0, -50.0);

UPDATE threshold
SET value = .4
WHERE id = 1;

CREATE TABLE IF NOT EXISTS profit_curve
(
  id serial NOT NULL,
  loss INTEGER,
  threshold DOUBLE PRECISION
);

COPY profit_curve(loss, threshold)
FROM '/mnt/c/Users/kurtrm/projects/predicting_equipment_failure/src/static/data/thresh_losses.csv' CSV HEADER;