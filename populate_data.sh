curl -X POST -d '{"net_id":"st999","password":"password","email":"st999@cornell.edu","name":"Random Student"}' localhost:5000/api/students
curl -X POST -d '{"net_id":"pf999","password":"password","email":"pf999@cornell.edu","name":"Random Professor"}' localhost:5000/api/professors
curl -X POST -d '{"net_id":"mhw66","password":"password","email":"mhw66@cornell.edu","name":"Michael White"}' localhost:5000/api/students
curl -X POST -d '{"net_id":"laz37","password":"password","email":"laz37@cornell.edu","name":"Leon Zaruvinsky"}' localhost:5000/api/professors

curl -X POST -d '{"title": "Recording and Tracking of Social Insects In-Vitro", "professor_id": "laz37", "description": "We are interested in the potential of robot collectives for parallel task execution. Such systems are inspired by social insects in nature, where thousands of relatively simple individuals coordinate with no central point of control. Unfortunately, such colonies are notoriously hard to study and little is known about how they organize. Here, we will attempt to develop new tool sets to automatically gather large amounts of data to verify old or prompt new hypotheses. In other words, the goal is twofold; to design tools to help analyze and learn from social insects in nature, and using this knowledge to implement robotic swarms capable of long-term autonomous behavior in complicated real-life settings. <br><br>The students will device a system for gathering relevant visual data on several ant colonies in the lab. This will involve a practical setup with a computer for data collection and several HD webcams. The first part of the project involves developing software to perform running image analysis on incoming frames, and autonomously decide when snippets of video are worth storing, with the aim of collecting large amounts of relevant data automatically. The second part of the project involves automatically tracking unmarked ants in the recordings to provide additional information for analysis. The student will also be responsible (with guidance) for setting up these ant colonies and maintaining them throughout the semester. Weekly meetings will be held to assure progress of the project.", "tags": ["robotics", "databases"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Protohuman Project", "professor_id": "laz37", "description": "Artificial Intelligence is an evolving aspect of computer science. One thing that makes humans intelligent is our ability to learn from experience. Not only can we learn from our own experience, but also from experiences told to us by other people. In order to decide how much to trust this information, people need to form long-term relationships with each other. This is a first step toward forming communities. The focus of the proposed research is to develop a virtual world that contains autonomous agents that form relationships with each other and with people. These agents will be capable of simple communication with each other, passing information between the agents. This combination of social relationships and information passing will help form a community of autonomous agents inside the virtual world. Once it is developed, this virtual community may be used to study how humans form relationships.The software installation will be based on an existing research project called the Making Friends Project. The Making Friends Project uses a code base developed by the Synthetics Characters Group at the MIT Media Lab, with significant modifications by my faculty mentor and me. It is mostly written in Java and has a thin layer of C and C++ to communicate with the DirectX graphics. The Protohuman Project contributes to the areas of multi-agent systems, human-computer interaction, and interactive animation.", "tags": ["artificial intelligence", "algorithms", "machine learning"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Generalizing Emotional Memory", "professor_id": "laz37", "description": "The Generalizing Emotional Memory mechanism involves models of emotion, perception and learning. This implementation uses a very simple model of emotion. Each autonomous agent will have a single floatingpoint value for valence, which varies from 0.0 to 1.0. The system blends between example animations to give an expressive range to the behavior of the characters [3]. The characters disambiguate among their social partners by perceiving several attributes, which include a unique identification tag, color and size. The first thing that the autonomous agents perceive will be the attributes color and size. Then they will notice the identification tag. Finally, they will be able to perceive the Object of Attention of the partner. Each character may have one other character as its Object of Attention. Mutual attention (when two characters have each other as their Objects of Attention) defines the start and end of an interaction episode. After each interaction the character will revise the emotion and confidence values that are stored in its Generalizing Emotional Memories for each of the attributes – color, size and unique ID. When a character encounters a new social partner, it will begin a relationship with it based on the values in the GEMs for the correct color and size, even though it does not yet know anything about that partner’s unique ID.", "tags": ["artificial intelligence", "algorithms", "computer vision"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Safe GPU programming", "professor_id": "laz37", "description": "It’s no secret that GPUs are taking over from CPUs in some of the world’s most important computations, from machine learning to scientific computing to video games. But programming models for GPU code can be incredibly brittle and error-prone to work with. Especially when an application needs to integrate work on the CPU with work on the GPU, interoperation is typically verbose and unsafe in frameworks OpenGL and CUDA. <br><br>We have a new language approach to integrated programming on heterogeneous hardware called “static staging.” The idea is to let programmers mark the code that should be compiled for different units in a single program. We have a prototype of the language and compiler called Braid that currently compiles to OpenGL (really, JavaScript and WebGL). <br><br>Your task would be to extend this compile to work for general-purpose GPU computing by emitting CUDA or OpenCL code. <br><br>You should be familiar with and interested in compiler design and implementation. Some familiarity with GPU programming of any sort (OpenGL, OpenCL, DirectX, or CUDA) would be useful but is not required. The compiler is implemented in TypeScript, so familiarity with JavaScript would also be helpful.", "tags": ["algorithms", "machine learning"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Notebook Widgets for Simulation Steering and Monitoring", "professor_id": "laz37", "description": "Python has a long history as a system for steering large-scale physical simulations, and remains useful for this purpose today. In contrast, IPython notebooks are proving increasingly useful for managing and documenting small-scale simulations and data analysis tasks. I would like to have the best of both worlds by using an IPython notebook as the control panel for some of my simulation and optimization codes, sending control messages from a client notebook and receiving updates that can be accessed either from the Python environment or from an interactive visualization widget. Many of the pieces for this project are already there (e.g. in the IPython parallel module and the IPython interactive widget architecture), but they don’t quite do what I would like.", "tags": ["graphics", "theory", "natural language processing","algorithms","ethics"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Recording and Tracking of Social Insects In-Vitro", "professor_id": "pf999", "description": "We are interested in the potential of robot collectives for parallel task execution. Such systems are inspired by social insects in nature, where thousands of relatively simple individuals coordinate with no central point of control. Unfortunately, such colonies are notoriously hard to study and little is known about how they organize. Here, we will attempt to develop new tool sets to automatically gather large amounts of data to verify old or prompt new hypotheses. In other words, the goal is twofold; to design tools to help analyze and learn from social insects in nature, and using this knowledge to implement robotic swarms capable of long-term autonomous behavior in complicated real-life settings. <br><br>The students will device a system for gathering relevant visual data on several ant colonies in the lab. This will involve a practical setup with a computer for data collection and several HD webcams. The first part of the project involves developing software to perform running image analysis on incoming frames, and autonomously decide when snippets of video are worth storing, with the aim of collecting large amounts of relevant data automatically. The second part of the project involves automatically tracking unmarked ants in the recordings to provide additional information for analysis. The student will also be responsible (with guidance) for setting up these ant colonies and maintaining them throughout the semester. Weekly meetings will be held to assure progress of the project.", "tags": ["robotics", "databases"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Protohuman Project", "professor_id": "pf999", "description": "Artificial Intelligence is an evolving aspect of computer science. One thing that makes humans intelligent is our ability to learn from experience. Not only can we learn from our own experience, but also from experiences told to us by other people. In order to decide how much to trust this information, people need to form long-term relationships with each other. This is a first step toward forming communities. The focus of the proposed research is to develop a virtual world that contains autonomous agents that form relationships with each other and with people. These agents will be capable of simple communication with each other, passing information between the agents. This combination of social relationships and information passing will help form a community of autonomous agents inside the virtual world. Once it is developed, this virtual community may be used to study how humans form relationships.The software installation will be based on an existing research project called the Making Friends Project. The Making Friends Project uses a code base developed by the Synthetics Characters Group at the MIT Media Lab, with significant modifications by my faculty mentor and me. It is mostly written in Java and has a thin layer of C and C++ to communicate with the DirectX graphics. The Protohuman Project contributes to the areas of multi-agent systems, human-computer interaction, and interactive animation.", "tags": ["artificial intelligence", "algorithms", "machine learning"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Generalizing Emotional Memory", "professor_id": "pf999", "description": "The Generalizing Emotional Memory mechanism involves models of emotion, perception and learning. This implementation uses a very simple model of emotion. Each autonomous agent will have a single floatingpoint value for valence, which varies from 0.0 to 1.0. The system blends between example animations to give an expressive range to the behavior of the characters [3]. The characters disambiguate among their social partners by perceiving several attributes, which include a unique identification tag, color and size. The first thing that the autonomous agents perceive will be the attributes color and size. Then they will notice the identification tag. Finally, they will be able to perceive the Object of Attention of the partner. Each character may have one other character as its Object of Attention. Mutual attention (when two characters have each other as their Objects of Attention) defines the start and end of an interaction episode. After each interaction the character will revise the emotion and confidence values that are stored in its Generalizing Emotional Memories for each of the attributes – color, size and unique ID. When a character encounters a new social partner, it will begin a relationship with it based on the values in the GEMs for the correct color and size, even though it does not yet know anything about that partner’s unique ID.", "tags": ["artificial intelligence", "algorithms", "computer vision"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Safe GPU programming", "professor_id": "pf999", "description": "It’s no secret that GPUs are taking over from CPUs in some of the world’s most important computations, from machine learning to scientific computing to video games. But programming models for GPU code can be incredibly brittle and error-prone to work with. Especially when an application needs to integrate work on the CPU with work on the GPU, interoperation is typically verbose and unsafe in frameworks OpenGL and CUDA. <br><br>We have a new language approach to integrated programming on heterogeneous hardware called “static staging.” The idea is to let programmers mark the code that should be compiled for different units in a single program. We have a prototype of the language and compiler called Braid that currently compiles to OpenGL (really, JavaScript and WebGL). <br><br>Your task would be to extend this compile to work for general-purpose GPU computing by emitting CUDA or OpenCL code. <br><br>You should be familiar with and interested in compiler design and implementation. Some familiarity with GPU programming of any sort (OpenGL, OpenCL, DirectX, or CUDA) would be useful but is not required. The compiler is implemented in TypeScript, so familiarity with JavaScript would also be helpful.", "tags": ["algorithms", "machine learning"]}' localhost:5000/api/posts
curl -X POST -d '{"title": "Notebook Widgets for Simulation Steering and Monitoring", "professor_id": "pf999", "description": "Python has a long history as a system for steering large-scale physical simulations, and remains useful for this purpose today. In contrast, IPython notebooks are proving increasingly useful for managing and documenting small-scale simulations and data analysis tasks. I would like to have the best of both worlds by using an IPython notebook as the control panel for some of my simulation and optimization codes, sending control messages from a client notebook and receiving updates that can be accessed either from the Python environment or from an interactive visualization widget. Many of the pieces for this project are already there (e.g. in the IPython parallel module and the IPython interactive widget architecture), but they don’t quite do what I would like.", "tags": ["graphics", "scientific computing"]}' localhost:5000/api/posts