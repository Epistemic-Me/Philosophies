# Philosophies

A Philosophy is like a "plug-in" for Epistemic Me that provides a philsophical context in which users can start to clarify their beliefs.

It enables coaches and health practioners to focus on clarifying the philosophy they want to use to help their patients and coachees achieve real outcomes - rather than the technology that might enable that change.

Our current strategy is to use philosophies as a way to boostrap models of self of coaches and influencers we want on the Epistemic Me platform. This may change in the future as we move more processing to the backend.

## All Philosophers Welcome

*Any* practioner can easily to write a philosophy for Epistemic Me. However, Philosophies can also be written for more advanced professional use cases.

As an example, imagine a Functional Health practioner writing philosophy within Epistemic Me. A good philosophy, once plugged into the tool, would systematically help users clarify their health beliefs by applying the philosophy of Functional Medicine. Through reflective prompts, such as "What patterns do you observe between your symptoms and daily habits?" or "How do specific stressors or foods impact your energy levels?" it would guide users to identify underlying relationships between their lifestyle and well-being. By mimicking the structured approach of a Functional Medicine practitioner, this strategy would enable users to generate insights and hypotheses about their health in a systematic, belief-driven way—empowering them to take actionable steps consistent with Functional Medicine principles.

Practioners can also upload their own existing writing (soon podcasts and Youtube Videos) and have Epistemic Me generate a "Philosophy" automatically using a the concept of a "Meta Strategy": a writing that extracts the Epistemic Context from a piece of work and writes a philosophy that can be tweaked for Epistemic Me. 

## How To Add Your Own Philosophy

To add your own philosophy, simplify add new strategy in a markdown file and keep it in the `philosophies/` folder. We suggest taking a look at existing examples, and reading through the "MetaStrategy.md" to get a sense for what makes a philosophy that works well with Epistemic Me. 

You can also generate dialectic strategies dynamically through the Epistemic Me CLI.

As an example, to regenerate the "RespondAndDontReact" philosophy example you would use the following command. Read the docs of our CLI to learn more.

``epistemic create_dialectic_strategy resources/RespondAndDontReact.txt {{open_api_key}}``

