# Thematic Research Collections with Lenticular

Lenticular is a developer tool to create thematic research collections. These collections contain materials that are relelvant to a specific research project and outcomes such as a book, article or museum exhibit. Lenticular is focused primarily on research outcomes rather than preservation or presentation of project materials. Data can be packaged and exported to other tools for those purposes. 

Lenticular builds on the example of David Bamman's [BookNLP](https://github.com/booknlp/booknlp), which is a natural language processing pipeline to generate research data from novels. BookNLP processes a novel's text and returns structured data for analysis, including charachter name clustering, quotation speaker identification, event tagging and other metadata relevant to the literary analysis of a novel. BookNLP turns raw text into structured research data. 

Lenticular offers a similar pipline for processing and packaging research collections. These types of processes are usually handled by large companies such as [Gale](https://www.gale.com/intl/archives-explored/behind-the-scenes/creating-a-digital-archive-technical) or ad hoc by researchers using the skills and resources at hand. Research collections can include document images, audio files, video, or text. We gather and organize materials, process them with OCR and LLMs, and package them for analysis and publication as data. We also generate a static website that can be used to research the collection.


### Fetching project materials
- Download materials from Box, British Library, Drive...
- Organize and normalize file names and directory structure

### Processing and metadata production
- OCR with Vision transformer/Noughat 
- OCR post-processing with LLMs
- text correction (given Tesseract,Nougat output, create a corrected version ; perhaps MM-LLM with image as input)
  - summary 
  - metadata generation
  - embedding generation 
  - entity recognition and linking 
### Quality control
  - ...metrics for OCR, LLM performance
  - [Datasheets for datasets](https://arxiv.org/abs/1803.09010)
  - [Model cards](https://huggingface.co/docs/hub/model-cards)
### Packaging and Publishing of data 
- HugginFace-style. Parquet (package as exchange file HF-Hub)
- GitHub repo-style. Directory and files (image, metadata, text, embeddings, etc.)

### Packaging as static website 
The static site can be accessed in the browser. It builds from the examples of [Collection Builder](https://collectionbuilder.github.io/) and [Wax](https://minicomp.github.io/wax/). It also provides research functionality more like [Google pinpoint](https://journaliststudio.google.com/pinpoint/about), [Talk to Books](https://books.google.com/talktobooks/) and [Palladio](https://hdlab.stanford.edu/palladio/).
-  Search Index with [PageFind](https://pagefind.app/)
- Collection description
  - Collection metadata / features
  - topic modeling, clustering, etc.
  - [Atlas-style](https://atlas.nomic.ai/) visualization page
  - Recommended topics, arguments, relevance to existing knowledge
6. Research interface
  - "Talk to PDF" style bot to interact with the collection? Would need [LangChain.js](https://js.langchain.com/docs/get_started/introduction) 
