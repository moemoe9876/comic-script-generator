# modular_agents/script_generator.py
import sys
import json
from typing import Dict

import google.generativeai as genai

import config


class ScriptGenerator:
    """
    Generates a YouTube script from a story summary.
    """
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,  # Higher temperature for more creative outputs
            top_p=0.9,       # Allow more diverse token selections
            top_k=40,        # Consider more token options
            max_output_tokens=4096,
        )
        self.model = genai.GenerativeModel(
            config.GENERATIVE_MODEL_NAME,
            generation_config=generation_config
        )

    def generate_script(self, story_summary: str) -> Dict[str, str]:
        """
        Generates a YouTube script from a story summary using advanced narrative techniques.
        
        Args:
            story_summary (str): The comic story to adapt into a script
            
        Returns:
            Dict[str, str]: Dictionary containing the script, title suggestions, and word count
        """
        prompt = f"""
        
        --
        You are an expert YouTube scriptwriter specializing in comic book summaries. Your goal is to convert a story analysis into an engaging, fast-paced script. Follow these steps precisely.
        
        **CRITICAL INSTRUCTION - READ THIS FIRST:**
        You MUST use ONLY the story provided below. DO NOT use any other Marvel stories from your training data. DO NOT improvise or add characters/events not mentioned in the provided story. Stick strictly to the actual comic book story given to you.


        - Third-person narrative, present tense
        - Direct, conversational tone like the examples
        - Clear chronological story progression
        - Similar sentence structure and flow
        - Same level of detail and pacing
        - CRITICAL: Use simplistic language and words, do not overcomplicate sentences.
        - Do not include dialogue that is within the comic in the script, for example, do not include: "(dialogue from a character)" 
        
        **MUST FOLLOW INSTRUCTIONS BELOW**

        📏 **OPTIMAL SCRIPT LENGTH**
        - Target: 200-300 words exactly (proven optimal for YouTube shorts)
        - First 30 words must hook viewer attention
        - Maintain steady pacing throughout
        - End with strong resolution in final 30-40 words
        - Count words carefully as you write
        
        🎯 **STORY ARCHITECTURE**
        - Opening Hook (10-15% of word count)
           • Pose intriguing question or setup
           • Create immediate emotional investment
           • Promise compelling payoff
        
        - Rising Action (50-60% of word count)
           • Build tension systematically
           • Layer complications
           • Deepen character stakes
        
        - Climax (20-25% of word count)
           • Deliver emotional peak
           • Resolve main conflict
           • Provide satisfaction
        
        - Resolution (10-15% of word count)
           • Tie emotional threads
           • Leave lasting impression
           • Encourage sharing/engagement
        
        📝 **EFFICIENCY GUIDELINES**
        - Every sentence must serve multiple purposes:
          • Advance plot
          • Reveal character
          • Build emotion
          • Create anticipation
        - Cut any word that doesn't contribute to these goals
        - Maintain momentum while being thorough
        - Focus on emotional truth over minor details
        
        ⚡ **SENTENCE STRUCTURE RULES**:
           1. Use coordinating conjunctions to link ideas: "And while...", "But when...", "And after..."
           2. Mix short punchy sentences with longer descriptive ones
           3. Use "only for/to" pattern for dramatic reversals
           4. End paragraphs with cliffhangers or revelations
           5. Every sentence must be efficient and advance the plot
        
        🗣️ **LANGUAGE REQUIREMENTS**:
           - Use simple, conversational words (avoid: "subsequently", "furthermore", "nevertheless")
           - When the story calls for it, use direct, gritty, or blunt language—choose words like "slept with" instead of euphemisms such as "intimate with" to maintain authenticity and impact.
           - Prefer active voice: "Batman finds Joker" not "Joker is found by Batman"
           - Use contractions naturally: "he's", "they're", "won't"
           - Include casual expressions: "pretty much", "just in time", "all of a sudden"
           - For emotional stories: Focus on emotional resonance over action
        
        📝 **NARRATIVE VOICE**:
           - Third-person, present tense ONLY
           - Omniscient narrator who knows character thoughts and feelings
           - Tone matches the emotional context of the story
           - Never break the fourth wall or address the reader directly

        📚 **STORY STRUCTURE REQUIREMENTS**:
           - OPENING: Hook viewers with the initial conflict/setup (2-3 sentences)
           - DEVELOPMENT: Cover all major plot points in chronological order
           - CHARACTER MOMENTS: Include key character interactions and emotional beats
           - CLIMAX: Build to and fully describe the story's climactic moment
           - RESOLUTION: Complete the story with proper conclusion
        
        🚫 **ABSOLUTE PROHIBITIONS**:
           - NO direct character dialogue in quotes
           - NO comic book sound effects (BAM, POW, etc.)
           - NO overly complex vocabulary
           - NO narrator commentary about the story being fictional
           - NO passive voice overuse
           - NO skipping major story elements to save word count
        
        ✅ Use appropriately emotional language when needed — convey deep feelings without being melodramatic
        ✅ Flow seamlessly from sentence to sentence
        ✅ Build emotional tension throughout the narrative
        ✅ Include specific comic book details and character actions
        ✅ End with emotional impact that resonates beyond the video
        ✅ Ensure every major plot point from the story summary is covered
        --
        **SUCCESSFUL SCRIPT EXAMPLES:**

        Understand how each example utilises simplistic language and the same flow while delivering an engaging script. Utilise the structure and and language chosen onto your work
        
        Example 1 - "How Did Dr Doom Take Over The World?":
"After sorcerer Supreme Dr. Doom took over the world, he put an end to all senseless wars and promised every citizen free universal healthcare, leaving the Avengers with no other choice but to stop him. After gathering every useful hero available and Squirrel Girl, the Avengers arrive at Laaria to end Doom's reign, only to be completely humiliated in front of the whole world. As time went on and people's lives began to change for the better, Doom's followers started to grow in number. While the Avengers are desperately trying to come up with a plan to stop him, believing that Doom has every world leader under some form of mind control, Carol comes up with a plan to free them from Doom's influence. And while she believes that the Avengers are more than powerful enough to beat Victor, she's called in a few villains to help them. With the help of their new allies, Captain Marvel plans to distract Doom while Scarlet Witch frees every world leader from his mind control. And with everyone on board, they arrive at the Lavarian border once again. Having anticipated their arrival, Doom welcomes the Avengers with his dinosaur variant. And while he's surprised that Earth's mightiest heroes were desperate enough to team up with a group of villains, he reassures them that they stand no chance of winning. While the Avengers are keeping Doom distracted, Scarlet Witch enters the mind of every politician under Doom's influence. But after spending hours trying to break their mind control, she's shocked to learn the truth. Despite what they thought, Doom didn't use his powers to control the politicians. He simply offered to give them whatever they needed to gain their support, money, power, or drugs."

Example 2 - "How Spider-Man Almost Ended Peter Parker?":
"How did Spider-Man almost get Peter Parker killed? While Peter is out on a date with MJ, they are interrupted by a giant tric sentinel destroying Manhattan. MJ asks if he needs to get out of here, but Peter doesn't think he'll have to because Spider-Man is already there to deal with it. A few days ago, Peter went to visit Dr. Connors at the university to discuss the isotope genome accelerator, the device that gave him his powers all those years ago. Connors explains that with the accelerator's help, he plans to separate his human side from the lizard, but their talk is cut short by Taskmaster and Black Ant, who came to steal the device. Taskmaster throws Peter out of the way, only for him to accidentally turn on the accelerator, separating Spider-Man and Peter Parker from each other. Once Spider-Man has dealt with the villains, he and Peter swing away to talk about what just happened. But after realizing that they can finally live separate lives, Spidey goes to do some superhero stuff, leaving Peter alone on the rooftop. Without his powers, Peter can finally live a normal life. He can go back to school and settle down with the woman he loves. All while Spider-Man is having the time of his life, going on talk shows, and making millions of dollars with various sponsorships. But when he starts to swing people around the city for money, Peter decides it's time to have a talk. Realizing that the experiment left Spider-Man with no sense of responsibility or intellect, Peter tries to remind him of why they decided to become heroes in the first place, only for Spidey to web him to a wall and swing away. Knowing that he needs to get his powers back or somebody will get hurt, Peter steals the accelerator from Dr. Connors lab, but when he tries to turn everything back to normal, they are attacked by an army of Tsentinels. As they try to run away, a sentinel behind them is about to blow both of them up, only for Peter to save Spider-Man's life by pushing him away. Lying half dead on the ground, Peter hopes that Spider-Man has finally learned to be more responsible. But since it didn't really work, he activates the accelerator with his web shooter, merging their bodies back"

Example 3 - "Deadpool Takes Spider-Man To Hell #spiderman #shorts":
"While Spider-Man is fighting with Hydroman, Deadpool interrupts them, telling Spidey that his villains are very boring. And after giving him a hug, Wade teleports both of them to hell, where they're captured by Dormamu. As Deadpool continues to annoy Spider-Man with his jokes, Peter asks Dormamu if he can torture them separately, buying Wade just enough time to dislocate his hip and cut themselves loose. When Dormamu's mindless ones attack them, Wade is confused why Spidey is angry with him, saying he only wanted to give him a battle worthy of an Avenger. But when even Dormamu questions why Spider-Man would team up with an idiot like Deadpool, Wade ends the battle by giving the mindless ones brains, causing them to turn against their master. Thinking that this must be a bad dream, Spider-Man tells Deadpool to immediately take them home. But by the time they arrive, Hydroman has absorbed all the water from the sewers, demanding $100 million or he'll drown the city in its own filth. After getting blasted with sewer water, Deadpool blames Spider-Man for unleashing a walking toilet on the city. But when Peter asks if he has any grenades on him, he throws Wade into Hydroman, causing both of them to explode. While Deadpool's legs are starting to grow back, Spider-Man cleans his suit on a rooftop. But as he gets ready to leave, Wade asks to hear him out for a second. Deadpool explains that he's been trying to change and thought that if he spent more time with Spider-Man, he could start to earn his respect. But knowing that it probably won't happen, Wade jumps off the roof while Peter swings away, saying that he needs a lot of therapy."

Example 4 - "The Flash Helps Superman's Victim #injustice #shorts":
"After the defeat of Injustice Superman, the heroes who stood by his side are facing the consequences of their actions. Clark is held in a red sun prison, Wonder Woman is facing trial on Thasera. And while Flash managed to avoid being arrested thanks to turning against Superman at the last second, he is forbidden from ever using his powers again. Barry Allen arrives at the longest straight road in Australia, a place he once considered to be paradise. But as he sets off on his 90-m long journey, a truck in front of him loses control. Without thinking about the consequences, Barry saves the driver's life. And when Batman calls him, having already seen what happened, he tells Barry to stay out of trouble and agrees to let this one go. As Barry continues his journey, he remembers the time he met Mitchell Davies, one of his biggest fans, who later became the hero Gixor in hopes of following in his idol's footsteps. But when Superman and his regime arrived in Australia to disperse a peaceful protest, Gixor tried to make them leave, only for Clark and Diana to break his back while Flash stood there and did nothing. After days of painful walking, Barry finally reaches Mitchell's home where his mother Laura greets him. And when Barry explains that he came to help his son walk again, she takes him to his room. Barry introduces himself as the Flash, and after calling Gixur a hero for standing up to Superman, he apologizes for not doing the same when he had the chance. Barry tells Mitchell that he's been learning a lot about his condition, and if he'll allow him, he'd like to help him walk"

Example 5 - "How Did A Gift Drive Batman Insane? #batman #shorts":
"How did a gift drive Batman insane? Many years ago, during his second encounter with the Joker, Batman received a very special birthday gift that blew up right in his face. Ever since that day, Joker set aside time from his busy schedule to surprise his friend with a new present every month. Just like the Joker, these presents were unique and different every time. Sometimes they were violent and vicious or harmless and bizarre. And while it has never been on Batman's actual birthday, he could count on receiving one every month until he didn't. For the whole month, Batman's been patiently waiting to receive his present. Wondering what twisted joke is waiting for him this time. But on the last day of the month, with only hours left until midnight, Bruce still hasn't received his gift. Knowing that the Joker is hiding somewhere, planning his next big surprise, Batman does everything he can to find him before somebody gets hurt. He checks in with every old friend, crawls through the sewers, and even asks Superman for help, only for Joker to show up 1 hour before midnight, wishing him a happy birthday. For weeks, Bruce had obsessed over what the Joker might do next. Prepared for every scenario and driven himself to the brink of insanity, trying to stay one step ahead. And as he stands there with a big smile on his face, Batman finally snaps. Bruce attacks him, trying to break every bone in Joker's body while demanding his birthday present. But after seeing his friend almost become as crazy as he is, Joker tells him that the gift he prepared is a simple reminder that they're going to do this forever."

Example 6 - "Who's The Voice Inside Deadpool? #deadpool #shorts":
"Who's the voice inside Deadpool's head? While on a mission to eliminate a lawyer called Matt Murdoch, Deadpool is interrupted by a stranger in a weird costume who boops him in the nose. Not liking to be booped, Wade removes the man's head, who simply catches it in his hand, and after introducing himself as Mad Cap, declares war on Deadpool. Wade shifts his focus back to shooting the lawyer, only for Daredevil to show up and kick both of them in the head. Not having the time for healing factor guys, Daredevil calls in Thor for help, who accidentally disintegrates both of them into a pile of ash. As Deadpool begins to regenerate, he notices that Madcap is gone when he suddenly hears a strange new voice inside his head. Thinking that Mad Cap put the voice inside his head to annoy him, Deadpool wanted to get rid of it at first, but as time went on, he started to like it more and more. When Deadpool is hired once again to assassinate Murdoch, now fully aware he's Daredevil, he distracts the surrounding heroes by planting a bomb nearby, only for Luke Cage to show up with his bomb, offering to shove it up Wade's ass. Deadpool attacks him with every weapon he can find. But after Luke breaks his knee and punches his face in, the voice inside Wade's head takes over, Madcap explains that after Thor turned them into a pile of ash, their bodies got mixed together. And while Deadpool's been steering the ship so far, it's his turn to have some fun. Simply by looking at him, Madcap forces Luke Cage to dance uncontrollably. And when Thor arrives to stop him, the same happens to the Asgardian as well. While the two heroes are busy dancing with each other, Wade comes up with a plan to remove Mad Cap from his head. And after asking Thor and Luke if they like tugof-war, they rip Deadpool's body exactly in half. Once they're fully healed, admitting that it was pretty fun while it lasted, Madcap leaves Wade on his own, promising to call him in the future."

Example 7 - "Deadpool is...Scared? #deadpool #shorts":
"While Taskmaster is training with Deadpool's daughter, Ellie, who recently got her powers, Doug interrupts their sparring session, bringing an urgent message from Wade's latest archeneemy, Deathgrip, inviting the mercenary to his temple to settle their unfinished business. Surprised by the weirdly named villain's invitation, Deadpool happily accepts it. And after promising Ellie that he'll be back by the end of the next issue, he and Taskmaster head out to deal with Death Grip. Deadpool kicks the door open, only for his head to catch on fire. And as Taskmaster begins to shoot deathgrip students with his arrows, Wade asks if they have any idea how expensive it is to get a new mask made. As they start to get outnumbered by the goons, Deadpool asks Taskmaster to try holding them off while he finds Death Grip. And although Tony agrees to do it, he tells Wade to hurry up so they can go home. Deadpool finds his new friend meditating alone. And after hitting him in the head with a gun, he gets ready to end their rivalry as quickly as it started. But simply by touching his chest, Death Grip nullifies Wade's healing factor. As Wade begins to cough up blood, Deathgrip asks if he's already run out of jokes to say, and to see if his plan really worked, slashes Deadpool's chest wide open with his hand. Deathgrip explains that after underestimating the mercenary during their last fight, he located the Muramasa Blade, the weapon that can neutralize any healing factor, and took its power into himself. Realizing that he may have underestimated his opponent, a strange feeling comes over Wade, a feeling he hasn't felt since he got his powers. Fear."

Example 8 - "The Joker is In a Coma #joker #shorts":
"The Joker is dying and the doctors at Arkham call on Ray Palmer, the atom, as their last hope to save him. Dr. Francis explains that a rare condition is causing Joker's synapses to fire non-stop and if left untreated, he'll die. But Ry is not sure why that would be a problem. The doctors insist they have a moral obligation to save every patient, even the Joker. And the only solution is to inject a compound directly into his brain at a microscopic level. Not sure why he should bother, Adam refuses. But when they explain there's a chance the procedure might kill the Joker, Ray asks where he can sign up. With the compound in hand, Ray enters Joker's brain through his nose. And after he enters the bloodstream, he stops for a second to think about how terrible it would be if he accidentally caused a blood clot. Shrinking further to fit into the synaptic gaps, Ry arrives at the root of the problem. But as he prepares to administer the compound, a lightning bolt hits him, pulling him into one of Joker's memories. Ray watches as a young Joker is confronted by three bullies, demanding that he move from their spot. But after some careful consideration, Joker decides to beat one of them to death with his lunchbox. Later that day, Joker overhears his parents arguing about his behavior at school. And after packing his belongings, he sets their house on fire, leaving them both trapped inside. As Ray goes deeper and deeper into the madman's memories, he sees Joker on a rooftop, telling one of his victims how much he loves his job. Joker sees himself as an artist destined to remake the world in his own image. He believes that one day he'll succeed in making the world as mad as it made him. And on that day, he can finally die in peace. Ray snaps out of the nightmare and contemplates letting the clown die. But thanks to the Joker's insanely strong plot armor, Adam decides to give him the cure instead. Because if he died, Batman would be very sad."

Example 9 - "How Did The Thing Get His Powers Back? #fantasticfour #shorts":
"How did the Thing get his powers back? After sorcerer Supreme Dr. Doom cured Ben Grim of his condition to prove he could do in seconds what Richards couldn't in decades, the rest of the Fantastic Four are doing everything they can to help Ben get his powers back. Reed explains that in order for it to work, Ben would need to be exposed to the exact same cosmic rays that transformed them all those years ago. But with time travel off the table, Franklin suggests they travel to another universe where the Fantastic 4 are just about to get their powers. After the smartest man alive got outsmarted by his 15-year-old son, they all rush to the Baxter building and within hours they arrive in an alternate reality where their counterparts lives are about to change forever. As the cosmic rays are approaching, Ben gets ready to turn back to his old rocky self. And while Sue shields the rest of them from the storm, he gets exposed to its full power. After the other Fantastic 4 return to Earth, their powers kick in just as they were supposed to. But unfortunately for Ben, nothing's changed. As they continue to travel from universe to universe, they watch different versions of the Fantastic 4 get transformed. Some look just like them, others are completely different. But no matter what world they visit, the outcome's always the same. The team gets their powers while Ben gets nothing. Realizing that the cosmic rays from alternate universes won't work, Ben secretly alters their next destination, sending them to their own universe just moments before they got their powers. As the ship nears the storm, Ben gets ready to be exposed to its full power. And as his body finally starts to transform, he happily tells the others that it worked. But when their past selves return to Earth, they remain completely unchanged. Without their powers, the Fantastic 4 was never created. Reed and Sue never got married, and Franklin and Valyria were never born, leaving them all to fade out of existence."

Example 10 - "Joker vs Every Robin Over The Years #joker #shorts":
"Joker is crying in his cell, but when his therapist asks him to get serious, he offers to tell them another story that will twist their guts about a good friend of his, Robin, the boy wonder. This poor kid is put into harm's way every night by that lunatic Batman who forces him to go unarmed against Gotham's worst criminals when he should be doing his homework. The therapist asks Joker if he's concerned for Robin's well-being, but he simply wants to kill him, which he has managed to do at least once. Over the years, Joker had countless encounters with the boy wonder and watched as he grew into a man. Then one day, he was gone. For a long time, Joker wondered what could have happened to him. Did he get a real job or did he settle down? Or perhaps a worse fate befall the boy wonder. A few months went by with Batman going solo. Then when he least expected it, a new Robin showed up, and Joker really liked this one. When he finally captured this new Robin, he was ever so surprised, but not half as surprised as when Joker beat him to death with a crowbar, then blew him up just to make sure. After Jason Todd's death, Joker finally had Batman all to himself. But after getting the crap kicked out of him over and over again, he began to grow bored. He's lost his passion and was just going through the motions until another Robin showed up out of the blue. Joker's world was rocked to its core, wondering how many more times he had to kill the brat. The more he thought about it, the less sense it made, which usually wouldn't bother him. But this time, it did until a very pleasant thought occurred to him. There was more than one Robin. He either killed the others or they retired. And if that's true, then perhaps there was more than one Batman. Maybe he did succeed in killing him all those times."

Example 11 - "Deadpool Humbles Rhino #deadpool #shorts":
"After Deadpool is hired by an old man to steal something from Rhino, convinced it will cure his ED, Wade kicks the door open with a chainsaw in his hand, but he's instantly thrown out of the house. As he's flying towards the restaurant across the street, Deadpool gets a call from Mr. Whitaker's wife, offering him $250,000 to leave the horn and do nothing. Before he can respond, the old man calls him, telling Wade not to listen to that painted harlot. Deadpool dusts himself off and walks back to Rhino's house, shooting all of his friends, only to be thrown out again. WDE's phone rings again and Mrs. Whitaker offers him half a million dollars to leave, which he happily accepts. As he tries to get into his car and leave, an annoyed Rhino starts to chase him. Deciding that it's time to retreat, Deadpool jumps onto a nearby motorcycle, telling the rider that unless he's Galactis under his leather jacket, he'd better drive fast. He arrives at his headquarters, rushing downstairs to his collection of Avengers memorabilia. He throws on Hulk's pants and Iron Man's boots, hoping they'll give him an edge. But when Rhino catches up, the pants prove to be useless. As his final chance for survival, Deadpool resorts to spraying Rhino with Ant-Man's shrinking gas, reducing him to a miniature size. As the negotiations continue, the old man ups the bid to $1 million. And after grabbing a saw, Deadpool apologizes to Mini Rhino, but some rich idiot wants his fake little horn. Wade delivers the horn to Mr. Whitaker, telling him and his wife that they are both seriously screwed up. He puts a gun on the desk, telling them to either fix their marriage or get a permanent divorce. As he walks away, feeling pretty optimistic about the two of them, he hears a loud bang. He returns home to find a very angry mini rhino waiting for him. Wade hands him an Oreo."

Example 12 - "The Truth About Batman's New Girlfriend #batman #shorts":
"Batman's new girlfriend has a dark secret. When Bruce Wayne runs into his childhood friend, Scarlett Scott, who now works as a geneticist at Wayne Techch, she takes him to her lab, excited to show him her latest project. Scarlet introduces Sangrail, a drug she created to significantly extend human lifespan. But since it will always be too expensive for the average person, she wants Bruce to be one of the lucky few to take it, arguing that some lives are worth more than others. Even though that statement goes against everything Bruce believes in, he's tempted to take it, wondering what more he could accomplish if his body wasn't held back by aging. And after hearing Superman's opinion, he decides to go through with it. After taking the drug for the first time in decades, Bruce slept for 11 hours straight. And when Damian woke him up worried that something is wrong with him, they get a call from Oracle telling them there's a murder they should investigate. At the crime scene, they find that the victim's body was completely drained of blood. And when a mysterious crew shows up to take the body away, Batman and Robin politely ask who they are working for. After beating them unconscious, Batman scans their ID card. And when the name Sarra comes up, Bruce invites Scarlet to dinner, hoping to rule her out as a suspect. After spending the night together, Bruce borrows the files on Scarlet's computer. But when he arrives home, he finds a letter on his gate containing the truth about his new girlfriend. More than 20 years ago, the night Scarlet was born, her father got into a terrible car crash. And if it weren't for Bruce's father, Thomas Wayne, he would have died. After a 9-hour long surgery, Thomas saved the man's life, not knowing that by doing that, he'd just signed his and his wife's death sentence. Because the man he saved that night was none other than Joe Chill."

Example 13 - "Deadpool's New Job: Multiversal Hitman #deadpool #shorts":
"After Deadpool defeated every hero and villain on Earth, he finds himself all alone thinking about what he's done. When Enthman interrupts him, asking Wade to say something funny, not being in the mood for jokes, Deadpool quickly takes care of the old man. But when he turns around, he sees a woman congratulating him. She introduces herself as Alfie. But before she could explain the reason she came here, Wade immediately passes on the opportunity and walks away. Not liking his answer, Alfie suggests to continue the conversation in her office. And after seeing tens of thousands of dead Deadpools in front of him, Wade changes his mind. As Alfie begins to explain the importance of what they're about to do, Deadpool tells her to just give him the target's name. After she hands him a device to freely travel across the multiverse and the list of people he'll need to eliminate. Wade gets on with finding his first victim. Deadpool shoots Spider-Man from afar, but he easily dodges the bullet. And when Alfie notes that he missed, Wade tells her that it's all part of his plan. Alfie tells Deadpool that the Spider-Man he's fighting is actually Dr. octopus who switched bodies with Peter Parker. And as Wade very quickly finds out, this Spider-Man is not holding back. After blowing Deadpool's brains out, Superior Spider-Man swings away, thinking that the fight is over. But when he ignores his spider sense, the explosives Wade hid in his costume goes off. Once Spider-Man's remains hit the ground, Deadpool asks for a new mask and continues to go through his list. But when he sees his next victim, Wade knows that he's in trouble. Hulk is surprised to see Deadpool, telling him that he's supposed to be dead. And although Wade tries to attack him, he quickly realizes that this was a bad idea. Deadpool tries to teleport away as fast as he can, but Hulk grabs his arm. And after smashing him into the ground, he prepares to do something to Wade he won't be able to regenerate from. But before he could do that, he vanishes."

Example 14 - "The Joker's Surprisingly Fun Day #joker #shorts":
"When Joker meets a boy called Sergio, the kid is happy to see him, thinking that his dad hired him as a clown for his birthday. Joker decides to play along. And when he sees Sergio torturing insects for fun, he asks if he can join in. As Joker rips the leg off a bug, he asks Sergio if he ever kills them. But the kid only does that when they try to escape because if they're dead, he can't play with them anymore. Surprised by the boy's wisdom, Joker asks where the guests are. But Sergio tells him that nobody came to his birthday because every kid in the neighborhood thinks he's a freak. Joker tells the boy that everybody's a freak. Some people just try to hide it. And after telling Sergio to get ready for the best birthday ever, he goes out to handle the invitations. Joker breaks into every house in the neighborhood, politely asking the families to attend Sergio's birthday or he'll blow their brains out. While the guests are all singing happy birthday with a big smile on their faces. Sergio blows out his candles and when his father Ameliano arrives, Joker suggests they talk in the kitchen. Joker reminds him that they had a job yesterday and since Ameliano didn't show up, he came here to kill him. But after thinking about the wisdom his son shared with him, Joker tells Ameiliano to hold out his hand and cuts off his fingers. After serving the fingers to the kids as hot dogs, Joker gets ready to leave, promising he'll be back next year. But when he walks out the door, Sergio runs over to him with his bug box in hand. As a thank you for the amazing birthday party, the boy wants Joker to keep his torture bugs. And after giving Sergio a big hug, Joker promises to only kill them if they try to escape."

Example 15 - "Eddie Brock's New Friend #carnage #shorts":
"After Eddie Brock bonded with Carnage, he finds himself sitting on a plane while his new friend encourages him to kill everyone on board. Once Eddie takes his meds, Carnage reminds him to focus on the reason they are here, to catch a serial killer. To help with finding the man they're looking for, Carnage enters the mind of every passenger. But after going through all their memories, Eddie realizes that the killer is one of the pilots. They walk to the cockpit and with a little help from his friend, Eddie rips the door clean off when Carnage suggests killing both pilots just to be safe. But the co-pilot stabs his colleague and after making sure the plane goes down with him, Carnage rips the man to pieces. As Carnage can't wait to see the plane crash into the ocean, Eddie kicks the door open. And after grabbing every passenger, they fly away just in time. But since he has a reputation to uphold, the symbiote takes control of Eddie's body and does what needs to be done. The next morning, Eddie wakes up in his bed, not knowing how he got here or what happened to the passengers, telling Carnage it's time to talk face to face. Eddie demands an explanation for what happened yesterday, but after thinking about it for a second, Carnage refuses. Eddie starts to threaten him, but Carnage shows him just how powerless he is, telling Brock that there is only one way to get rid of him, and they both know he won't do it. Carnage reminds Eddie that it was his idea for them to bond, thinking he could control the symbiote. And although they agreed to only go after serial killers, he's insulted that Brock thought he would keep his word. Having wasted enough of their precious time, Carnage tells Eddie that it's time to find their next victim. But this time, he wants someone who can put up a fair fight."

Example 16 - "Spider Man and Human Torch's Trip To The Waterpark #spiderman #shorts":
"Johnny Storm is fed up with Spider-Man, tired of seeing his face everywhere he goes. So, he visits Reed in his lab, telling him they need to boost their popularity. Richards casually hands him the cure for acne, saying it should help. But when Franklin walks in wearing a Spider-Man hat, Johnny get annoyed and decides to meet up with Spidey at the usual place. Johnny explains that ever since their last battle with Dr. Doom, people have been calling them traitors and loose cannons. Since Spider-Man used to be the most hated superhero in New York, Johnny came here to ask how he manages to get through the day as a complete loser. Spider-Man is speechless, asking how an idiot like him survived this long. And as Peter gets ready to choke him to death, Homeland Security tells them to immediately get off the Statue of Liberty. As Johnny flies him home, Spider-Man agrees to give him a few tips and they meet up at the local water park the next day. While wearing a disguise, Spider-Man tries to get people's attention by shouting Johnny's name. And just like he intended, the crowd begins to confront Human Torch for being a terrible superhero. As more and more people start to gather around them, Peter's spider sense goes off and Hydroman attacks them. As the entire water park begins to flood, Spider-Man tries to save the bystanders. And while Johnny takes off his wet clothes that are weighing him down, Hydroman hits them with a massive wave. Johnny ends up in the kids pool with no pants on. And to save the children from lifelong trauma, Peter quickly gives him a web speedo, only for it to instantly melt when he flames on. As the fight with Hydroman continues, Johnny storms into the women's bathroom with a flaming Johnson while Ben watches the events unfold on the TV, wondering how his day could get any Better."

Example 17 - "Deadpool Breaks Into X-Men Island #deadpool #shorts":
"When Deadpool gets angry at the X-Men for not inviting him to their fancy new island, Wade takes matters into his own hands and decides to go there anyway. While Wade is blown away by how beautiful this place is, he gets rudely interrupted by the X-Men, asking what he's doing here. Deadpool calls them a bunch of fus for excluding him until magic breaks his nose and takes him to see Emma Frost. Wade tells her that all he asks for is unlimited visits to Krakcoa and the cure for cancer and he'll be on his way. Emma agrees that as a friend of the X-Men, he should have been invited to visit the island a long time ago. But despite what he's heard, she's sorry to say that they don't have the cure for cancer, knowing not to expect too much from the X-Men, Deadpool says it's fine. But since there's a 97% chance he would burn this place to the ground if he stayed, Emma asks Wade to leave. After calling them a bunch of jerks and fists, Deadpool agrees to leave. But when he tries to take a flower with him as a souvenir, Wolverine stabs him in the back. As the X-Men attack him, Wade tells them that he only came here because he didn't want to be excluded. And as revenge for breaking his nose, he punches Magic in the face. When Rogue breaks up the fight, she tells Wade that she's sorry they can't cure him, offering to let him keep the flower, but Deadpool drops it to the ground because he doesn't need their pity. Wolverine says that it's not pity, just friendship. But Wade notes that the way they beat the [ __ ] out of him a few minutes ago didn't seem very friendly. And after calling them all fat one last time, Deadpool decides to leave. After going home, Deadpool and Jeff decide that if they can't go to KCOA, they will build their own island where there is only one rule."

Example 18 - "Spider-Man Saves Tomorrow #spiderman #shorts":
"Peter Parker wakes up on a Monday morning excited to get the week started because for the first time in his life, everything is going his way. He arrives at Horizon Labs where he meets up with his colleague Grady, who can't wait to show Peter his latest invention, a doorway that lets you travel 24 hours into the future. Peter is skeptical at first, but when Grady walks through the portal and hands him a newspaper from tomorrow, he decides to try it as well, only to find New York completely destroyed in the future. Peter rushes back to the present, borrowing the newspaper Grady brought from the right future, telling him that all they have to do is make sure that everything that's supposed to happen happens and tomorrow is saved. While going through the list of what he's supposed to do today, Spider-Man stops a super villain's rampage, delivers a baby, and even breaks Daredevil's record of catching 11 purse snatchers in a day. While Peter is trying to save tomorrow, Mayor Jameson welcomes Silver Sable to their first annual Saran Pride parade. But in a nearby alley, Flag Smasher plans to destroy the whole event with a nuclear bomb. Spider-Man teams up with Silver Sable to take down Flag Smasher, and thanks to his spider sense, Peter easily deactivates the bomb. After Sable thanks him for saving her people, Peter goes on with his plan to save New York until MJ calls him, asking if he wants to grab dinner. Spider-Man says he's busy right now, but when MJ jokes that the world won't end if she has to eat alone, Peter immediately joins her, worried that the world will end if she has to eat alone. With 25 minutes left until New York's supposed destruction, Peter is anxiously checking his watch when MJ tells him that whatever he's dealing with, she knows that Peter Parker will figure it out. Realizing exactly what he needs to do, Peter leaves MJ at the diner and rushes back to Horizon Labs, telling Grady that all they had to do was to turn off the portal."

Example 19 - "How Did Joker Escape From The Chair? #batman #shorts":
"How did the Joker get off death row? After Joker was arrested for allegedly poisoning people with stamps laced in Joker venom, his lawyer suggests to go for the insanity plea as they usually do. When the trial begins, Joker's lawyer argues that his client is in need of therapy, not punishment, telling the jury that the face they see before them is not the face of sanity. But after the judge deems Joker competent enough, he calls him to take the stand. Joker claims to be innocent, but when the district attorney asks if he's aware of the clever crimes he's being accused of, he gets deeply offended. To his lawyer's shock, Joker begins to list all the crimes he's done over the years, calling himself the Einstein of crime, saying that the person who committed the stamp murders is an amateur at best. When the jury is about to deliver the verdict, Joker is confident he'll walk free, only to be found guilty on all accounts, receiving the death penalty. The next day, Joker is taken to Blackgate prison, and once he's shown to his cell, his lawyer comes for a visit. Joker tells him that he wants the fast lane to the electric chair, fearing that people will stop caring about him soon. And if the state delays his execution, he'll sue them for millions of dollars. With 36 hours left until the big day, Joker is given a fresh haircut. And as his final meal, he requests a fruit salad with strawberries. After he finished confessing his sins to a priest, Joker is taken to the electric chair with a big smile on his face. Excited for the world to witness his final words. But when the warden tells him that the event won't be televised, Joker attacks the guards. Once they manage to strap him to the chair, the warden gets a call from the governor ordering them to immediately halt the execution. After Batman found the real killer and presented the evidence to the authorities, Joker is taken back to Arkham happier than he's ever been until Bruce reminds him that from now on, every breath he takes, he owes it to That man."
        ---
        **COMIC STORY TO ADAPT:**
        {story_summary}
        {transcript_context}
        ---

        Generate:
        **WORD COUNT CHECK:** Count your words before finalizing. Must be 200-300 words exactly.
        **SCRIPT:** [Your complete 200-300 word script draft - count every word]
        **TITLE SUGGESTIONS:** [3-5 title suggestions]
        **FINAL WORD COUNT:** [State the exact word count of your script]
        """

        response = self.model.generate_content(prompt)
        raw_text = response.text
        
        try:
            script_part = raw_text.split("**SCRIPT:**")[1].split("**TITLE SUGGESTIONS:**")[0].strip()
            titles_part = raw_text.split("**TITLE SUGGESTIONS:**")[1].split("**FINAL WORD COUNT:**")[0].strip()
            
            # Try to extract word count if present
            word_count = "Not specified"
            if "**FINAL WORD COUNT:**" in raw_text:
                try:
                    word_count = raw_text.split("**FINAL WORD COUNT:**")[1].strip().split('\n')[0].strip()
                except:
                    word_count = "Could not extract"
            
            return {
                "script": script_part,
                "title_suggestions": titles_part,
                "word_count": word_count
            }
        except IndexError:
            return {
                "script": "Error: Could not parse the script from the model's response.",
                "title_suggestions": "No titles generated.",
                "raw_response": raw_text
            }

if __name__ == '__main__':
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Generate a script from a story summary.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python script_generator.py "path/to/your_comic/summary.txt" -o "script.json"

This will save 'script.json' inside the 'your_comic' directory.
If -o is omitted, the script will print JSON to standard output.
"""
    )
    parser.add_argument("summary_file", nargs='?', default=None, help="Path to the story summary file (e.g., 'output/comic_name/summary.txt'). If not provided, an empty summary is used.")
    parser.add_argument("-t", "--transcript", help="Path to an optional transcript file for context.")
    parser.add_argument("-o", "--output", help="Name for the output directory. If not provided, a directory will be created based on the summary file name or a default name.")

    args = parser.parse_args()

    try:
        summary = ""
        summary_path = None
        if args.summary_file:
            summary_path = Path(args.summary_file)
            if not summary_path.is_file():
                print(f"Error: Summary file not found at {summary_path}", file=sys.stderr)
                sys.exit(1)

            with open(summary_path, 'r', encoding='utf-8') as f:
                summary = f.read()

        transcript_content = None
        if args.transcript:
            transcript_path = Path(args.transcript)
            if not transcript_path.is_file():
                print(f"Error: Transcript file not found at {transcript_path}", file=sys.stderr)
                sys.exit(1)
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript_content = f.read()

        generator = ScriptGenerator()
        result = generator.generate_script(summary, transcript=transcript_content)

        output_dir_name = args.output
        if not output_dir_name:
            if summary_path:
                output_dir_name = summary_path.stem
            else:
                import datetime
                output_dir_name = f"script_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        output_dir = Path(output_dir_name)
        output_dir.mkdir(parents=True, exist_ok=True)

        md_content = f"# Script\n\n{result['script']}\n\n# Title Suggestions\n\n{result['title_suggestions']}"
        md_file_path = output_dir / "script.md"

        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ Script and titles saved to {md_file_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)