# Dialectical Strategies
A Dialectical Strategy is like a "plug-in" for Epistemic Me that helps prompt users to examine their beliefs within a specific framework or approach to understanding them. It enables coaches and health practioners to focus on clarifying the philosophy they want to use to help their patients and coachees achieve real outcomes - rather than the technology that might enable that change.

Any practioner can choose to write a dialectic strategy for Epistemic Me. 

For example, imagine a Functional Health practioner writing Dialectic Strategy within Epistemic Me. A good dialectic strategy, once plugged into the tool, would systematically help users clarify their health beliefs by applying the philosophy of Functional Medicine. Through reflective prompts, such as "What patterns do you observe between your symptoms and daily habits?" or "How do specific stressors or foods impact your energy levels?" it would guide users to identify underlying relationships between their lifestyle and well-being. By mimicking the structured approach of a Functional Medicine practitioner, this strategy would enable users to generate insights and hypotheses about their health in a systematic, belief-driven way—empowering them to take actionable steps consistent with Functional Medicine principles.

Practioners can also upload their own existing writing, Youtube Videos, or public facing work, and have Epistemic Me generate a "Dialectic Strategy" automatically using a the concept of a "Meta Strategy": a writing that extracts the Epistemic Context from a piece of work and writes a Dialectic Strategy that can be tweaked for Epistemic Me. 

## How To Add Your Own Dialectical Strategy

To add your own Dialectic Strategy, simplify add new strategy in a markdown file and keep it in the `strategies/` folder. We suggest taking a look at existing examples, and reading through the "MetaStrategy.md" to get a sense for what makes a Dialectic Strategy that works well with Epistemic Me. 

You can also generate dialectic strategies dynamically through the Epistemic Me CLI.

As an example, to regenerate the "RespondAndDontReact" Dialectic Strategy example you would use the following command. Read the docs of our CLI to learn more.

``epistemic create_dialectic_strategy resources/RespondAndDontReact.txt {{open_api_key}}``

