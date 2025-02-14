# Final Task - Report

## Requirements
- Develop final project with defense, report, and source code.
- Possible ideas: Algorithms for creating / managing schedule in university or work, Chess Bot, text message analysis for identifing inappropriate terms / lexicon, accounting for geographic data (cartographic roads, bus stops, timings and transport path analysis), attack detection system, image processing and upscaling, biometric authentication with deepfake attack prevention, real estate market analysis, recognition of hydraulic structures, image stabilization, human pattern recognition, natural speech processing and sythesis, etc.

## Solution
Topic: Geocoding and GIS data analysis with AI and address normalization / generation
1. [Geocoding](https://en.wikipedia.org/wiki/Address_geocoding) - task for converting or searching addresses or some title / name / description for specific location to the particular coordinates on the map. In the other hand, we have reverse geocoding, that does the opposite.
2. This task is highly related on the both NLP (Natural Language Processing) and vector / spatial data analysis.
3. In modern days, it could be solved with vast amount of toolkit and technologies: from LLM, SLM, just tokenizers, parsers, embeddings, etc.

Installation:
```
docker compose up
cat ./data/source_dump.sql | docker exec -i postgres_final psql -U postgres
- llama-cpp-python:
    - create seperate venv ```python3 -m venv venv_llama``` (because version of dependencies can cause some bugs with GPU acceleration)
    - install or reinstall with ```CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir``` or ```CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir```
    - for server api inference - ```pip install llama-cpp-python[server]```
    - run server api inference - ```python3 -m llama_cpp.server --config_file <config_file or config file path>```
```
