## Structured Scene-Graphs & Constraint Solving for Robust Text-to-3D Room Layouts.
Natural-language descriptions of interior scenes offer an intuitive interface for users, but LLM alone struggle to satisfy detailed spatial constraints without producing overlapping or out-of-bounds placements. In this work, we present a pipeline that decouples high-level planning from low-level execution by first having an LLM generate a structured scene-graph in JSON (furniture dimensions, room geometry, and relational rules). A fast CP-SAT solver then converts those declarative constraints into precise (x, y) coordinates on a 1 cm grid, guaranteeing collision-free
layouts. Next, a Blender Python template consumes the JSON and placements to instantiate primitives, set up an isometric camera and lighting, and render a 1920x1080 PNG. Finally, an optional Vision-LLM verification step (GPT-4V) checks whether the rendered image matches the user’s textual intent. Although our approach leveraged a constraint-aware JSON schema to define precise spatial relationships, the translation of these high-level constraints into accurate 3D placements remains a challenging step. This gap highlights promising opportunities for improving the integration between declarative spatial constraints and their faithful execution in rendering pipelines.

Link to [technical report](https://github.com/divinrkz/agentic-scene-graph/blob/main/Final_Report.pdf). <br>

![Agentic Pipeline](https://github.com/divinrkz/agentic-scene-graph/blob/main/assets/agent-lifecylce.png?raw=true)

--------------------
## Contributors 
- Favour Okodgbe (@favourokodogbe)
- Chigozirim Ifebi (@CheeChizzle)
- Eden Obeng Kyei (@eobengky)
- Divin Irakiza (@divinrkz)
  

