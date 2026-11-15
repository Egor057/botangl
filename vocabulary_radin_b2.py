"""База текстов для чтения уровня B2 (10 текстов по ~3000-3500 символов и 10 вопросов к каждому)."""

READING_PASSAGES_B2 = [
    {
        "id": "b2_1",
        "short_title": "1. 🌐 Этика искусственного интеллекта",
        "title": "Text 1: The Complex Ethical Landscape of Artificial Intelligence in Society",
        "text": (
            "As artificial intelligence systems transition from experimental laboratories into the foundational infrastructure "
            "of modern global society, humanity faces a profound philosophical and regulatory reckoning. Algorithms now dictate "
            "credit approvals, medical diagnoses, judicial sentencing recommendations, and the curation of news consumed by "
            "billions daily. Proponents argue that machine learning models offer unprecedented efficiency, objectivity, and "
            "scalability, capable of processing multi-dimensional datasets beyond human cognitive limits. However, critics and "
            "ethics researchers urgently highlight that AI systems are fundamentally trained on historical human data, "
            "meaning they frequently absorb, codify, and amplify systemic societal prejudices. When an automated hiring tool "
            "systematically penalizes resumes containing female-associated names or minority dialects, it is not exhibiting "
            "malice; rather, it is mirroring the unaddressed historical biases embedded within its training corpus.\n\n"
            "Furthermore, the opacity of deep neural networks—often referred to as the 'black box' problem—complicates the quest "
            "for corporate and legal accountability. When a self-driving vehicle makes a catastrophic error or an algorithmic "
            "underwriting model denies a life-saving loan, tracing the exact chain of computational causality back to a human "
            "responsible party can prove nearly impossible. This accountability gap threatens to erode public trust in automated "
            "institutions. To navigate this treacherous territory, international policymakers, computer scientists, and ethicists "
            "are advocating for stringent regulatory frameworks focused on algorithmic transparency, mandatory bias auditing, "
            "and 'explainable AI' initiatives. Ultimately, technology is never neutral; it is a direct amplification of human "
            "intentions, cultural values, and institutional priorities."
        ),
        "questions": [
            {"type": "choice", "question": "What domains do AI algorithms currently influence according to the text?", "options": ["Credit approvals, medical diagnoses, and judicial sentencing", "Only weather forecasting and video games", "Exclusively manufacturing machinery", "Domestic cooking and gardening"], "correct": "Credit approvals, medical diagnoses, and judicial sentencing"},
            {"type": "open", "question": "Write a short sentence: Why do AI systems frequently codify societal prejudices?", "sample": "Because they are trained on historical human data containing those biases."},
            {"type": "choice", "question": "What does an automated hiring tool do when it penalizes certain resumes?", "options": ["It mirrors unaddressed historical biases in its training corpus", "It acts out of malicious intent", "It operates completely randomly", "It follows direct human orders in real time"], "correct": "It mirrors unaddressed historical biases in its training corpus"},
            {"type": "open", "question": "Write a short sentence: What term is used to describe the opacity of deep neural networks?", "sample": "It is referred to as the black box problem."},
            {"type": "choice", "question": "Why is tracing computational causality difficult in deep neural networks?", "options": ["Because of the opacity and complexity of black box models", "Because computers lack electricity", "Because code is always written in secret languages", "Because humans refuse to inspect logs"], "correct": "Because of the opacity and complexity of black box models"},
            {"type": "open", "question": "Write a short sentence: What does the accountability gap threaten to erode?", "sample": "It threatens to erode public trust in automated institutions."},
            {"type": "choice", "question": "What solutions are policymakers and ethicists advocating for?", "options": ["Algorithmic transparency, mandatory bias auditing, and explainable AI", "Banning all computers worldwide", "Leaving software entirely unregulated", "Replacing humans with robots in government"], "correct": "Algorithmic transparency, mandatory bias auditing, and explainable AI"},
            {"type": "open", "question": "Write a short sentence: According to the text, is technology ever neutral?", "sample": "No, technology is never neutral."},
            {"type": "choice", "question": "What do proponents claim machine learning models offer?", "options": ["Unprecedented efficiency, objectivity, and scalability", "Complete elimination of human error forever", "Free energy for everyone", "Absolute moral perfection"], "correct": "Unprecedented efficiency, objectivity, and scalability"},
            {"type": "open", "question": "Write a short sentence: What do AI systems amplify alongside human intentions?", "sample": "They amplify cultural values and institutional priorities."}
        ]
    },
    {
        "id": "b2_2",
        "short_title": "2. 🧬 Эволюционная биология",
        "title": "Text 2: The Evolutionary Significance of Epigenetics and Gene Expression",
        "text": (
            "For over a century following the rediscovery of Gregor Mendel’s foundational laws of inheritance, mainstream genetics "
            "was dominated by a rigid, deterministic paradigm: DNA was viewed as an immutable master blueprint, and living organisms "
            "were passive vehicles executing its coded instructions. Environmental factors might influence survival rates through "
            "natural selection across generations, but an individual's personal life experiences were presumed incapable of altering "
            "their hereditary genetic material. However, the revolutionary emergence of epigenetics over the past two decades has "
            "shattered this deterministic worldview, revealing a dynamic, responsive layer of molecular control that sits directly "
            "above the static DNA sequence.\n\n"
            "Epigenetics investigates how external environmental stimuli—ranging from chronic psychological stress, nutritional "
            "deficits, and airborne toxins to physical exercise and social deprivation—can chemically modify gene expression without "
            "altering the underlying nucleotide sequence. These biochemical modifications primarily occur through DNA methylation "
            "and histone modification, acting like microscopic molecular dimmer switches that either silence specific genes or "
            "enhance their transcription. Crucially, groundbreaking longitudinal studies suggest that certain epigenetic adaptations "
            "acquired during an individual's lifetime can under specific conditions be heritable, passed down to subsequent "
            "generations. This profound biological flexibility demonstrates that organisms are in a continuous, active dialogue with "
            "their surrounding environment, bridging the historic artificial divide between nature and nurture."
        ),
        "questions": [
            {"type": "choice", "question": "How was DNA viewed in mainstream genetics for over a century?", "options": ["As an immutable master blueprint", "As a flexible and constantly changing fluid", "As an unimportant biological byproduct", "As a synthetic chemical structure"], "correct": "As an immutable master blueprint"},
            {"type": "open", "question": "Write a short sentence: What has shattered the genetic deterministic worldview?", "sample": "The revolutionary emergence of epigenetics has shattered it."},
            {"type": "choice", "question": "What does epigenetics investigate?", "options": ["How external environmental stimuli chemically modify gene expression", "How stars are formed in deep space", "How ancient languages evolve over time", "How financial markets crash during pandemics"], "correct": "How external environmental stimuli chemically modify gene expression"},
            {"type": "open", "question": "Write a short sentence: What are two examples of external stimuli mentioned?", "sample": "Chronic psychological stress and nutritional deficits."},
            {"type": "choice", "question": "Through what primary mechanisms do epigenetic modifications occur?", "options": ["DNA methylation and histone modification", "Nuclear fission and atomic decay", "Cellular combustion and evaporation", "Magnetic resonance and gravity waves"], "correct": "DNA methylation and histone modification"},
            {"type": "open", "question": "Write a short sentence: What do epigenetic modifications act like?", "sample": "They act like microscopic molecular dimmer switches."},
            {"type": "choice", "question": "What can certain epigenetic adaptations acquired during a lifetime be?", "options": ["Heritable and passed down to subsequent generations", "Completely erased within one hour", "Visible on human skin immediately", "Transferred via digital communication"], "correct": "Heritable and passed down to subsequent generations"},
            {"type": "open", "question": "Write a short sentence: What does this biological flexibility bridge?", "sample": "It bridges the historic artificial divide between nature and nurture."},
            {"type": "choice", "question": "Who established foundational laws of inheritance mentioned in the text?", "options": ["Gregor Mendel", "Charles Darwin", "Albert Einstein", "Louis Pasteur"], "correct": "Gregor Mendel"},
            {"type": "open", "question": "Write a short sentence: What are living organisms no longer viewed simply as?", "sample": "They are no longer viewed simply as passive vehicles executing instructions."}
        ]
    },
    {
        "id": "b2_3",
        "short_title": "3. 💰 Поведенческая экономика",
        "title": "Text 3: Behavioral Economics and the Illusion of Human Rationality",
        "text": (
            "Classical economic theory was built upon the elegant yet deeply flawed assumption of 'Homo economicus'—the notion "
            "that human beings are rational, self-interested agents who consistently process available market information to "
            "maximize their personal utility and financial welfare. For decades, economic models treated market anomalies, "
            "bubbles, and sudden crashes as inexplicable deviations from normal rational equilibrium. However, the pioneering "
            "work of behavioral economists like Daniel Kahneman, Amos Tversky, and Richard Thaler radically dismantled this "
            "dogma by demonstrating that human decision-making is systematically warped by cognitive biases, emotional heuristics, "
            "and environmental framing effects.\n\n"
            "Behavioral economics reveals that our minds rely on two distinct systems of thought: System 1, which is fast, "
            "instinctive, emotional, and prone to systematic error; and System 2, which is slow, deliberate, analytical, and "
            "metabolically exhausting. Because the human brain consumes immense energy when performing deep rational calculations, "
            "individuals constantly default to mental shortcuts. Phenomena such as loss aversion—where the psychological pain "
            "of losing a hundred dollars vastly outweighs the joy of winning the same amount—explain why amateur investors "
            "panic during market downturns. Understanding these predictable psychological quirks has revolutionized not only financial "
            "markets and public policy design through 'nudging', but also consumer marketing strategies worldwide."
        ),
        "questions": [
            {"type": "choice", "question": "What was the core assumption of classical economic theory?", "options": ["Human beings are rational, self-interested agents", "Humans always act randomly in markets", "People are purely altruistic and selfless", "Economic markets are completely unpredictable"], "correct": "Human beings are rational, self-interested agents"},
            {"type": "open", "question": "Write a short sentence: What term describes the economic model of human rationality?", "sample": "It is called Homo economicus."},
            {"type": "choice", "question": "Who pioneered the field of behavioral economics mentioned in the text?", "options": ["Daniel Kahneman, Amos Tversky, and Richard Thaler", "Isaac Newton and Galileo Galilei", "Sigmund Freud and Carl Jung", "Adam Smith and Karl Marx"], "correct": "Daniel Kahneman, Amos Tversky, and Richard Thaler"},
            {"type": "open", "question": "Write a short sentence: How is human decision-making systematically warped?", "sample": "It is warped by cognitive biases, emotional heuristics, and framing."},
            {"type": "choice", "question": "What are the characteristics of System 1 thought?", "options": ["Fast, instinctive, emotional, and prone to error", "Slow, deliberate, and analytical", "Completely logical and mathematical", "Dormant during sleep"], "correct": "Fast, instinctive, emotional, and prone to error"},
            {"type": "open", "question": "Write a short sentence: Why do individuals constantly default to mental shortcuts?", "sample": "Because deep rational calculations consume immense metabolic energy."},
            {"type": "choice", "question": "What is loss aversion?", "options": ["When pain of losing money outweighs joy of winning it", "The desire to lose weight through dieting", "Forgetting where you put your wallet", "A corporate strategy to reduce tax burdens"], "correct": "When pain of losing money outweighs joy of winning it"},
            {"type": "open", "question": "Write a short sentence: How has understanding psychological quirks influenced public policy?", "sample": "It influenced policy design through the concept of nudging."},
            {"type": "choice", "question": "How did classical economists treat sudden market crashes?", "options": ["As inexplicable deviations from normal rational equilibrium", "As predictable mathematical certainties", "As deliberate government interventions", "As illusions created by media"], "correct": "As inexplicable deviations from normal rational equilibrium"},
            {"type": "open", "question": "Write a short sentence: Which system of thought is slow and analytical?", "sample": "System 2 is slow, deliberate, and analytical."}
        ]
    },
    {
        "id": "b2_4",
        "short_title": "4. 🌍 Геополитика изменения климата",
        "title": "Text 4: The Geopolitical Complexities of Global Climate Migration",
        "text": (
            "As global temperatures steadily rise and extreme weather events transition from once-in-a-century anomalies into "
            "predictable annual occurrences, the international community is forced to confront a profound humanitarian and "
            "geopolitical crisis: climate migration. Unlike traditional refugees fleeing political persecution or armed conflict, "
            "environmental migrants—often colloquially termed 'climate refugees'—are displaced by rising sea levels that swallow "
            "low-lying coastal archipelagos, persistent megadroughts that destroy agricultural livelihoods, and catastrophic "
            "ecosystem collapses that render entire regions uninhabitable. The World Bank estimates that unmitigated climate "
            "change could internally displace over two hundred million people by the middle of this century, primarily across "
            "sub-Saharan Africa, South Asia, and Latin America.\n\n"
            "This impending demographic shift poses immense challenges for international law and border security. Current global "
            "refugee conventions, established largely in the wake of the Second World War, legally recognize individuals fleeing "
            "persecution based on race, religion, or nationality, but offer zero protection or formal status to those fleeing "
            "ecological devastation. Consequently, displaced populations often fall into legal limbo, vulnerable to exploitation, "
            "statelessness, and xenophobic political backlash in destination countries. Addressing this crisis requires unprecedented "
            "diplomatic cooperation, robust climate adaptation funding for vulnerable nations, and a modern legal framework that "
            "recognizes environmental displacement as a shared global responsibility rather than an isolated national burden."
        ),
        "questions": [
            {"type": "choice", "question": "What are environmental migrants displaced by?", "options": ["Rising sea levels, persistent megadroughts, and ecosystem collapses", "Voluntary tourism and career changes", "Space exploration initiatives", "Industrial manufacturing relocations"], "correct": "Rising sea levels, persistent megadroughts, and ecosystem collapses"},
            {"type": "open", "question": "Write a short sentence: How many people could be internally displaced by mid-century?", "sample": "The World Bank estimates over two hundred million people."},
            {"type": "choice", "question": "Which regions are primarily affected according to the World Bank?", "options": ["Sub-Saharan Africa, South Asia, and Latin America", "Western Europe and North America", "Scandinavia and Antarctica", "Eastern Siberia and Greenland"], "correct": "Sub-Saharan Africa, South Asia, and Latin America"},
            {"type": "open", "question": "Write a short sentence: What do current post-WWII refugee conventions legally recognize?", "sample": "They recognize individuals fleeing persecution based on race, religion, or nationality."},
            {"type": "choice", "question": "What legal status do climate refugees currently receive under international law?", "options": ["Zero protection or formal status", "Permanent citizenship anywhere", "Full financial compensation", "Automatic diplomatic immunity"], "correct": "Zero protection or formal status"},
            {"type": "open", "question": "Write a short sentence: What vulnerability do displaced populations face in destination countries?", "sample": "They are vulnerable to exploitation, statelessness, and xenophobic backlash."},
            {"type": "choice", "question": "When were the current major global refugee conventions largely established?", "options": ["In the wake of the Second World War", "During the Roman Empire", "In the twenty-first century", "Following the invention of the internet"], "correct": "In the wake of the Second World War"},
            {"type": "open", "question": "Write a short sentence: What does addressing this crisis require diplomatically?", "sample": "It requires unprecedented diplomatic cooperation and climate funding."},
            {"type": "choice", "question": "What do extreme weather events represent today compared to the past?", "options": ["Predictable annual occurrences rather than rare anomalies", "Minor media exaggerations", "Completely ceased natural phenomena", "Secret government weather experiments"], "correct": "Predictable annual occurrences rather than rare anomalies"},
            {"type": "open", "question": "Write a short sentence: How should environmental displacement be recognized globally?", "sample": "It should be recognized as a shared global responsibility."}
        ]
    },
    {
        "id": "b2_5",
        "short_title": "5. 🔬 Нейропластичность мозга",
        "title": "Text 5: Neuroplasticity and Lifelong Cognitive Adaptation",
        "text": (
            "For decades, nineteenth and twentieth-century neuroscience operated under the dogmatic assumption that the adult "
            "human brain was a fixed, immutable biological machine. Medical orthodoxy dictated that neurological circuits were "
            "hardwired during early childhood development; once brain cells died or neural pathways were damaged by stroke or trauma, "
            "the central nervous system possessed zero capacity for regeneration or structural reorganization. This pessimistic "
            "dogma sentenced countless neurological patients to permanent disability. However, the groundbreaking discovery of "
            "neuroplasticity—pioneered by visionary researchers demonstrating that the brain constantly reorganizes itself by "
            "forming new neural connections throughout life—has completely revolutionized rehabilitation medicine and psychology.\n\n"
            "Neuroplasticity operates on a profound 'use it or lose it' principle at the microscopic synaptic level. When an individual "
            "acquires a complex new skill, such as playing a classical musical instrument, mastering a foreign language, or "
            "recovering motor functions after paralysis, physical gray matter density increases and neural pathways myelinate to "
            "optimize signal transmission speed. Conversely, unstimulating, passive routines cause unused synapses to undergo "
            "synaptic pruning. This dynamic malleability proves that cognitive decline is not an inevitable consequence of aging; "
            "rather, maintaining mental vigor, physical exercise, and continuous intellectual curiosity stimulates neurogenesis "
            "within the hippocampus, preserving cognitive resilience well into old age."
        ),
        "questions": [
            {"type": "choice", "question": "What was the historical medical assumption about the adult human brain?", "options": ["It was a fixed, immutable biological machine", "It grew new lobes every year", "It regenerated entirely every month", "It functioned identically to a computer CPU"], "correct": "It was a fixed, immutable biological machine"},
            {"type": "open", "question": "Write a short sentence: What did medical orthodoxy dictate about damaged neural pathways?", "sample": "It dictated that the nervous system possessed zero capacity for regeneration."},
            {"type": "choice", "question": "What does neuroplasticity mean for the adult brain?", "options": ["It constantly reorganizes itself by forming new neural connections", "It shrinks permanently after age twenty", "It stops consuming energy entirely", "It rejects all new memories"], "correct": "It constantly reorganizes itself by forming new neural connections"},
            {"type": "open", "question": "Write a short sentence: What principle does neuroplasticity operate on?", "sample": "It operates on a use it or lose it principle."},
            {"type": "choice", "question": "What physical change occurs when acquiring a complex new skill?", "options": ["Gray matter density increases and pathways myelinate", "Brain weight decreases by half", "Neural connections dissolve completely", "Skull bones expand in volume"], "correct": "Gray matter density increases and pathways myelinate"},
            {"type": "open", "question": "Write a short sentence: What happens to unused synapses during passive routines?", "sample": "They undergo synaptic pruning."},
            {"type": "choice", "question": "Is cognitive decline an inevitable consequence of aging according to the text?", "options": ["No, neuroplasticity and mental vigor help preserve cognitive resilience", "Yes, it is guaranteed by age thirty", "Only in individuals who never slept", "Yes, modern medicine has no effect on aging"], "correct": "No, neuroplasticity and mental vigor help preserve cognitive resilience"},
            {"type": "open", "question": "Write a short sentence: Where does continuous intellectual curiosity stimulate neurogenesis?", "sample": "It stimulates neurogenesis within the hippocampus."},
            {"type": "choice", "question": "What did the old pessimistic dogma sentence neurological patients to?", "options": ["Permanent disability with zero hope of recovery", "Instant miraculous healing", "Temporary memory loss only", "Mandatory musical training"], "correct": "Permanent disability with zero hope of recovery"},
            {"type": "open", "question": "Write a short sentence: What optimizes signal transmission speed in neural pathways?", "sample": "Myelination optimizes signal transmission speed."}
        ]
    },
    {
        "id": "b2_6",
        "short_title": "6. 📜 Эволюция письменности",
        "title": "Text 6: The Historical Evolution of Writing Systems and Human Memory",
        "text": (
            "The invention of writing stands as arguably the most transformative technological leap in human history, marking "
            "the definitive boundary between prehistory and recorded civilization. Before symbolic notation systems emerged in "
            "ancient Mesopotamia, Egypt, and China roughly five millennia ago, human knowledge was entirely ephemeral, preserved "
            "solely within the vulnerable biological confines of oral tradition and human memory. Sages, tribal elders, and "
            "bards carried the collective mythology, laws, and medicinal lore of their cultures, reciting epic poems from memory. "
            "However, oral cultures were inherently susceptible to drift, embellishment, and catastrophic loss if an entire "
            "generation was decimated by plague or warfare. The development of cuneiform script on clay tablets and hieroglyphs "
            "on papyrus allowed human thought to transcend the physical limitations of mortal lifespan.\n\n"
            "As the philosopher Socrates famously lamented in Plato's dialogues, the externalization of memory into written text "
            "sparked fierce intellectual anxiety, with critics arguing that literacy would atrophy human memory and foster "
            "the illusion of wisdom without true internal understanding. Yet writing achieved the exact opposite: by offloading "
            "repetitive data storage onto external mediums, human consciousness was liberated to engage in complex abstract "
            "reasoning, rigorous scientific inquiry, legal codification, and multi-generational philosophy. The written word "
            "transformed human culture from an isolated local echo into an accumulated, cumulative symphony of shared global intellect."
        ),
        "questions": [
            {"type": "choice", "question": "What boundary does the invention of writing mark in history?", "options": ["The definitive boundary between prehistory and recorded civilization", "The end of human technological innovation", "The transition from agriculture to nomadism", "The complete elimination of spoken language"], "correct": "The definitive boundary between prehistory and recorded civilization"},
            {"type": "open", "question": "Write a short sentence: Where was human knowledge preserved before writing systems?", "sample": "It was preserved entirely within oral tradition and human memory."},
            {"type": "choice", "question": "What vulnerability did purely oral cultures possess?", "options": ["Susceptibility to drift, embellishment, and catastrophic loss", "Immunity to historical inaccuracies", "Permanent digital preservation", "Instant worldwide communication"], "correct": "Susceptibility to drift, embellishment, and catastrophic loss"},
            {"type": "open", "question": "Write a short sentence: What early scripts are mentioned in the text?", "sample": "Cuneiform script on clay tablets and hieroglyphs on papyrus."},
            {"type": "choice", "question": "How did Socrates react to the invention of writing in Plato's dialogues?", "options": ["He lamented it, arguing literacy would atrophy human memory", "He celebrated it as humanity's greatest achievement", "He invented the alphabet himself", "He refused to speak to anyone who read books"], "correct": "He lamented it, arguing literacy would atrophy human memory"},
            {"type": "open", "question": "Write a short sentence: What anxiety did critics of literacy hold?", "sample": "They feared it would foster the illusion of wisdom without true understanding."},
            {"type": "choice", "question": "What did offloading data storage onto written mediums allow human consciousness to do?", "options": ["Engage in complex abstract reasoning and scientific inquiry", "Stop thinking entirely and rely on books", "Forget all historical events instantly", "Invent modern computer software"], "correct": "Engage in complex abstract reasoning and scientific inquiry"},
            {"type": "open", "question": "Write a short sentence: Approximately when did symbolic notation systems emerge?", "sample": "Roughly five millennia ago in Mesopotamia, Egypt, and China."},
            {"type": "choice", "question": "What did the written word transform human culture into?", "options": ["A cumulative symphony of shared global intellect", "A rigid, unchanging society of robots", "An isolated local echo with no future", "A purely numerical calculation system"], "correct": "A cumulative symphony of shared global intellect"},
            {"type": "open", "question": "Write a short sentence: What did cuneiform script allow thought to transcend?", "sample": "It allowed thought to transcend the physical limitations of mortal lifespan."}
        ]
    },
    {
        "id": "b2_7",
        "short_title": "7. 🌌 Философия науки",
        "title": "Text 7: Paradigm Shifts and the Philosophy of Scientific Revolutions",
        "text": (
            "For centuries, popular mythology and standard textbook pedagogy depicted scientific progress as a smooth, cumulative "
            "march of steady accumulation—a continuous process where scientists placidly gathered verified facts, added them to "
            "the towering edifice of human knowledge, and steadily edged closer to absolute objective truth. However, in his "
            "seminal 1962 treatise 'The Structure of Scientific Revolutions', philosopher and physicist Thomas Kuhn shattered this "
            "naive linear view, introducing concepts that permanently transformed our understanding of how science actually "
            "operates. Kuhn argued that scientific history is characterized by long periods of conservative 'normal science', "
            "punctuated by violent, destabilizing conceptual upheavals he termed scientific revolutions.\n\n"
            "During normal science, researchers operate entirely within an accepted theoretical framework or 'paradigm'—such as "
            "Newtonian mechanics or Ptolemaic astronomy—solving puzzles defined by that framework. When experimental anomalies "
            "accumulate to a degree that the reigning paradigm can no longer patch over or explain, a profound professional "
            "crisis ensues. This crisis culminates in a paradigm shift, where a radical new model—such as Einstein's relativity "
            "or quantum mechanics—sweeps through the scientific community. Kuhn famously asserted that competing paradigms are "
            "often 'incommensurable', meaning scientists operating within different frameworks literally interpret empirical "
            "data through entirely different conceptual lenses, proving that scientific objectivity is a complex, evolving human "
            "enterprise rather than a sterile mechanical calculation."
        ),
        "questions": [
            {"type": "choice", "question": "How did standard textbook pedagogy traditionally depict scientific progress?", "options": ["As a smooth, cumulative march of steady accumulation", "As a series of random chaotic explosions", "As stagnant and completely unchanging", "As entirely driven by financial greed"], "correct": "As a smooth, cumulative march of steady accumulation"},
            {"type": "open", "question": "Write a short sentence: Who authored the 1962 treatise 'The Structure of Scientific Revolutions'?", "sample": "Philosopher and physicist Thomas Kuhn authored it."},
            {"type": "choice", "question": "What did Thomas Kuhn argue characterizes scientific history?", "options": ["Long periods of normal science punctuated by revolutionary upheavals", "A completely unbroken line of permanent theories", "Purely accidental discoveries with no theory", "Constant war between scientists and philosophers"], "correct": "Long periods of normal science punctuated by revolutionary upheavals"},
            {"type": "open", "question": "Write a short sentence: What do researchers do during normal science?", "sample": "They operate entirely within an accepted theoretical framework or paradigm."},
            {"type": "choice", "question": "What triggers a profound professional crisis in science?", "options": ["The accumulation of unexplainable experimental anomalies", "A sudden shortage of laboratory glassware", "Government budget cuts across universities", "Scientists forgetting basic mathematics"], "correct": "The accumulation of unexplainable experimental anomalies"},
            {"type": "open", "question": "Write a short sentence: What event culminates from this scientific crisis?", "sample": "A paradigm shift sweeps through the scientific community."},
            {"type": "choice", "question": "What examples of radical new models are mentioned in the text?", "options": ["Einstein's relativity and quantum mechanics", "The steam engine and the printing press", "The theory of plate tectonics and DNA sequencing", "Microscopic germ theory and electricity"], "correct": "Einstein's relativity and quantum mechanics"},
            {"type": "open", "question": "Write a short sentence: What does incommensurable mean regarding competing paradigms?", "sample": "Scientists in different frameworks interpret data through different lenses."},
            {"type": "choice", "question": "What did Kuhn assert about scientific objectivity?", "options": ["It is a complex, evolving human enterprise", "It is a sterile mechanical calculation", "It does not exist in any form", "It was perfected by ancient Greeks"], "correct": "It is a complex, evolving human enterprise"},
            {"type": "open", "question": "Write a short sentence: What term did Kuhn use for conservative periods of research?", "sample": "He termed them normal science."}
        ]
    },
    {
        "id": "b2_8",
        "short_title": "8. 🏙️ Социология урбанизма",
        "title": "Text 8: Urbanization, Alienation, and the Sociology of Modern Cities",
        "text": (
            "The rapid, relentless urbanization of the human species represents one of the most dramatic demographic transformations "
            "in global history. For the first time in our existence, over half of the world's population resides within dense "
            "metropolitan centers, a proportion projected to approach seventy percent by the middle of the century. Early sociologists "
            "of the late nineteenth and early twentieth centuries, such as Georg Simmel and Louis Wirth, observed this emerging "
            "phenomenon with a mixture of awe and profound trepidation. Simmel, in his classic essay 'The Metropolis and Mental Life', "
            "argued that the sensory overload of city living forces urbanites to develop a psychological defense mechanism—a "
            "blunted, detached attitude termed the 'blasé outlook'—to cope with the relentless barrage of stimuli, noise, and strangers.\n\n"
            "While rural communities historically fostered tight-knit, intimate social cohesion based on shared kinship and "
            "tradition, the modern metropolis thrives on fleeting, anonymous encounters and hyper-specialized economic roles. "
            "This structural fragmentation can foster intense feelings of urban alienation and loneliness, even amidst physical "
            "crowds numbering in the millions. Yet cities simultaneously function as extraordinary crucibles of innovation, "
            "cultural hybridization, artistic expression, and social emancipation. The architectural and social density of "
            "metropolitan spaces forces diverse populations into creative friction, generating intellectual movements, democratic "
            "freedoms, and economic opportunities that have consistently propelled human civilization forward."
        ),
        "questions": [
            {"type": "choice", "question": "What proportion of the world's population currently resides in metropolitan centers?", "options": ["Over half of the world's population", "Less than ten percent", "Exactly ninety-nine percent", "Only people in wealthy nations"], "correct": "Over half of the world's population"},
            {"type": "open", "question": "Write a short sentence: What proportion is projected by mid-century?", "sample": "It is projected to approach seventy percent."},
            {"type": "choice", "question": "How did early sociologists like Simmel and Wirth view early urbanization?", "options": ["With a mixture of awe and profound trepidation", "With complete indifference and boredom", "With absolute hatred for all technology", "As a temporary trend that would soon reverse"], "correct": "With a mixture of awe and profound trepidation"},
            {"type": "open", "question": "Write a short sentence: What essay did Georg Simmel write about city life?", "sample": "He wrote 'The Metropolis and Mental Life'."},
            {"type": "choice", "question": "Why do urbanites develop the 'blasé outlook' according to Simmel?", "options": ["To cope with sensory overload, noise, and constant stimuli", "To become famous artists and writers", "To save money on public transportation", "To avoid paying municipal taxes"], "correct": "To cope with sensory overload, noise, and constant stimuli"},
            {"type": "open", "question": "Write a short sentence: What did rural communities historically foster?", "sample": "Tight-knit social cohesion based on kinship and tradition."},
            {"type": "choice", "question": "What does the modern metropolis thrive on?", "options": ["Fleeting, anonymous encounters and hyper-specialized economic roles", "Complete social isolation and zero commerce", "Agricultural self-sufficiency", "Identical lifestyles for every citizen"], "correct": "Fleeting, anonymous encounters and hyper-specialized economic roles"},
            {"type": "open", "question": "Write a short sentence: What negative feeling can structural fragmentation foster?", "sample": "It can foster intense feelings of urban alienation and loneliness."},
            {"type": "choice", "question": "How do cities function simultaneously alongside alienation?", "options": ["As extraordinary crucibles of innovation and cultural hybridization", "As useless historical relics of the past", "As quiet agricultural farming zones", "As military fortresses"], "correct": "As extraordinary crucibles of innovation and cultural hybridization"},
            {"type": "open", "question": "Write a short sentence: What does metropolitan architectural density force populations into?", "sample": "It forces diverse populations into creative friction."}
        ]
    },
    {
        "id": "b2_9",
        "short_title": "9. 🤖 Философия сознания",
        "title": "Text 9: Artificial Consciousness and the Philosophical Hard Problem",
        "text": (
            "As generative artificial intelligence systems display increasingly sophisticated linguistic fluency, creative problem-solving "
            "capabilities, and emotional mimicry, a mesmerizing philosophical debate has ignited across cognitive science and "
            "computer science: can a machine ever become truly conscious? Australian philosopher David Chalmers famously "
            "delineated the 'easy problems' of consciousness—such as explaining how the brain integrates sensory data, categorizes "
            "environmental stimuli, and controls behavioral output—from the 'hard problem': explaining why and how physical "
            "neural processing gives rise to subjective, qualitative inner experience. Why does processing red light feel like "
            "seeing red, rather than occurring as a cold, unconscious mathematical computation?\n\n"
            "While advanced large language models can convincingly simulate grief, joy, or philosophical introspection, functional "
            "simulation must never be conflated with genuine sentience. Current algorithms operate entirely through deterministic "
            "matrix multiplication and statistical weight adjustments across silicon transistors, utterly devoid of biological "
            "homeostasis, subjective vulnerability, or lived existential stakes. A supercomputer calculating poetry does not "
            "feel the melancholy of the verses any more than a digital thermometer feels the summer heat. If future synthetic "
            "architectures ever achieve true phenomenal consciousness, it will require an unprecedented paradigm shift far beyond "
            "mere computational scaling, forcing humanity to confront profound moral obligations toward artificial sentient beings."
        ),
        "questions": [
            {"type": "choice", "question": "What did philosopher David Chalmers delineate between?", "options": ["The easy problems and the hard problem of consciousness", "Hardware and software engineering", "Quantum mechanics and classical physics", "Human psychology and animal behavior"], "correct": "The easy problems and the hard problem of consciousness"},
            {"type": "open", "question": "Write a short sentence: What do the 'easy problems' of consciousness explain?", "sample": "They explain how the brain integrates sensory data and controls behavior."},
            {"type": "choice", "question": "What does the 'hard problem' of consciousness ask?", "options": ["Why and how physical neural processing gives rise to subjective inner experience", "How to write faster computer code", "How much electricity an AI server consumes", "Why humans invented mathematics"], "correct": "Why and how physical neural processing gives rise to subjective inner experience"},
            {"type": "open", "question": "Write a short sentence: What example of qualitative experience is mentioned?", "sample": "Why processing red light feels like seeing red."},
            {"type": "choice", "question": "What warning does the text give regarding functional simulation?", "options": ["Functional simulation must never be conflated with genuine sentience", "AI will destroy all human languages by next year", "Computers are already smarter than entire nations", "Silicon chips possess secret biological feelings"], "correct": "Functional simulation must never be conflated with genuine sentience"},
            {"type": "open", "question": "Write a short sentence: How do current AI algorithms operate entirely?", "sample": "Through deterministic matrix multiplication and statistical weight adjustments."},
            {"type": "choice", "question": "What are current AI algorithms utterly devoid of?", "options": ["Biological homeostasis, subjective vulnerability, and existential stakes", "Electricity and cooling fans", "Mathematical formulas", "Access to internet data"], "correct": "Biological homeostasis, subjective vulnerability, and existential stakes"},
            {"type": "open", "question": "Write a short sentence: Does a digital thermometer feel summer heat?", "sample": "No, just as a computer calculating poetry does not feel melancholy."},
            {"type": "choice", "question": "What would achieving true phenomenal consciousness require?", "options": ["An unprecedented paradigm shift far beyond computational scaling", "Simply adding more electricity to existing laptops", "Downloading a larger dictionary file", "Writing code in Python instead of C++"], "correct": "An unprecedented paradigm shift far beyond computational scaling"},
            {"type": "open", "question": "Write a short sentence: What would true machine consciousness force humanity to confront?", "sample": "Profound moral obligations toward artificial sentient beings."}
        ]
    },
    {
        "id": "b2_10",
        "short_title": "10. 🏛️ Экономика культурного наследия",
        "title": "Text 10: The Economics and Ethics of Cultural Heritage Preservation",
        "text": (
            "In an era characterized by hyper-globalization, digital homogenization, and relentless real estate development, "
            "historical city centers, archaeological monuments, and intangible cultural traditions face unprecedented pressures. "
            "Governments, international bodies like UNESCO, and local municipalities continually grapple with a complex economic "
            "and ethical dilemma: how to finance the preservation of cultural heritage without turning living communities into "
            "sterile, artificial museum exhibits or falling prey to aggressive 'over-tourism'. When a historic medieval town "
            "is converted entirely into souvenir shops, luxury hotels, and vacation rentals, its original inhabitants are priced "
            "out, stripping the historic core of its authentic social fabric and converting heritage into a hollow consumer commodity.\n\n"
            "Economists analyze heritage preservation through the lens of positive externalities and public goods, arguing that "
            "historical architecture and local traditions enrich national identity, foster social cohesion, and drive sustainable "
            "cultural tourism. However, maintenance costs are exorbitant, and private property owners often view stringent "
            "architectural regulations as oppressive financial burdens rather than civic privileges. Achieving a sustainable "
            "balance requires innovative public-private partnerships, community-led heritage management, and zoning laws that "
            "protect historical integrity while ensuring that local residents can afford to live, work, and thrive in their "
            "ancestral neighborhoods."
        ),
        "questions": [
            {"type": "choice", "question": "What forces create unprecedented pressures on cultural heritage today?", "options": ["Hyper-globalization, digital homogenization, and real estate development", "Lack of interest in history books", "Complete abandonment of all cities", "Excessive rainfall and wind erosion"], "correct": "Hyper-globalization, digital homogenization, and real estate development"},
            {"type": "open", "question": "Write a short sentence: What dilemma do governments and UNESCO grapple with?", "sample": "How to finance preservation without turning communities into museum exhibits."},
            {"type": "choice", "question": "What happens when a historic town converts entirely into vacation rentals?", "options": ["Original inhabitants are priced out, stripping its authentic social fabric", "The town becomes twice as wealthy permanently", "Historic buildings maintain themselves automatically", "Tourism instantly drops to zero"], "correct": "Original inhabitants are priced out, stripping its authentic social fabric"},
            {"type": "open", "question": "Write a short sentence: How do economists analyze heritage preservation?", "sample": "Through the lens of positive externalities and public goods."},
            {"type": "choice", "question": "What benefits do historical architecture and local traditions provide?", "options": ["Enrich national identity, foster social cohesion, and drive tourism", "Generate free electricity for neighboring towns", "Solve global economic inflation instantly", "Eliminate all traffic accidents"], "correct": "Enrich national identity, foster social cohesion, and drive tourism"},
            {"type": "open", "question": "Write a short sentence: How do private property owners often view stringent regulations?", "sample": "As oppressive financial burdens rather than civic privileges."},
            {"type": "choice", "question": "What are maintenance costs for historical heritage described as?", "options": ["Exorbitant", "Negligible and cheap", "Completely subsidized by tourists", "Decreasing every year"], "correct": "Exorbitant"},
            {"type": "open", "question": "Write a short sentence: What does achieving a sustainable balance require?", "sample": "Innovative public-private partnerships and community-led management."},
            {"type": "choice", "question": "What should zoning laws protect alongside historical integrity?", "options": ["That local residents can afford to live and work in ancestral neighborhoods", "Exclusive parking rights for foreign tourists", "The right to demolish old walls freely", "Maximum commercial profits for real estate developers"], "correct": "That local residents can afford to live and work in ancestral neighborhoods"},
            {"type": "open", "question": "Write a short sentence: What danger does aggressive over-tourism pose?", "sample": "It turns living communities into hollow consumer commodities."}
        ]
    }
]