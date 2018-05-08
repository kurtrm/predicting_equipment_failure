# Predicting Transformer Maintenance in the Atlanta Metropolitan Area

## Business Understanding
  Many businesses are forced to extend equipment life due to costs or extraneous situations that demand continued use.
Pumps, compressors, turbines, etc. have operating specifications, but their behavior may vary in the context of the systems they're embedded in, which may lead to unexpected or unpredictable failures. Given that these failures are commonplace, can we predict and therefore prevent equipment failure and subsequent plant shutdowns?

  Commercial plants or other intities that rely continual operation of heavy machinery would conduct this analysis in the interest of reducing overhead and thus preserving profits. However, government agencies or other entities that rely on rigid budgets rather than revenue generation may be more interested in preserving assets in order to carry out their unique purposes.
  
  The primary example here is the United States Navy. Given a set budget, the Navy is required to carry out its missions with whatever assets are available. In the case of strategic deterrence, there is a possibility that the entire strategic triangle can degrade if an SSBN suffers an equipment failure that requires it to abandon its primary mission.
  
  Thus, this analysis pivots away from the more traditional commercial intents of data science and instead focuses on:
  - Asset preservation
  - Cost reduction (arguably still a very commercial intent)

## Data Understanding
The data was obtained from bigml.com and consists of a year's worth of hourly logs on a piece of equipment. Though the machine and many of the headers have been obfuscated, this dataset replicates the logs that would be taken aboard a submarine or any other US Navy vessel. In addition, any kind of contract work would likely require this kind of obfuscation outside of a naval base, shipyard, or any other repair facility. The only additional data that would have been helpful is system-wide logs, not just logs on a single piece of machinery. Due to the interdependence and interactions of machinery in complex systems like a submarine, parameters from other parts of the system could be predictive for this piece of equipment. For example, a centrifugal pump may not have logs taken regarding bus frequency or voltage, and variations in these parameters may be indicative of failure.

## Data Preparation
The data has a time-series element to it, so any relevant columns were extracted with exception of hours_since_failure. Thus, the analysis was split into a time-series analysis and modeling on all other features.

## Modeling

## Evaluation

## Deployment
