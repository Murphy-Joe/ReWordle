# Inputs
- Guesses
- Clues from guesses
- Wordle's list of 2,309 possible answers ("common words" I refer to as "targets")
- Wordle's list of ~13,000 acceptable guesses ("dictionary words" I refer to as "playable guesses")



# Output
- A score that represents the narrowing ability of the next guess

# How 
- First off, do you really want to know all details in written form?
- If so, kudos to you and please email me, you're even more interested in this than I am
- Here's an abbreviated version

## Words Left
- First, filter the 2309 targets down to just the targets that meet the current clues
- example say thats 10 targets left

## Algorithm
### Goal
- Any one of the 10 targets remaining could be the right one.  
- So we want to know what type of playable guess would have good filtering results verse ALL the possible targets left. 
### Approach
* Take each one of the ~13,000 playable guesses and play each playable guess against a each target remaining. 
* Each time a guess is played against a target, we end up with a new amount of targets left.
    * If the guess matches the target that's 0 targets left
    * If the guess somehow provided no extra clues, that's 10 targets left
    * If the guess provided some new clues, that will be some number between 0 and 10
* After a guess is played against all the possible targets remaining, we can average the amount of words left it created when played against each target
* This average is referred to as the guess's "narrowing ability"
