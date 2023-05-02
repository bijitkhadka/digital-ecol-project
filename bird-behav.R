library(tidyr)
library(dplyr)
library(ggplot2)


dat = read.csv("~/uw-phd/classes/spring2023/digital-ecol/final-project/viddat.csv")

unique(dat$pre)
unique(dat$during)
unique(dat$post)
unique(dat$species)

## quickly count number of occurrences of behavior per column
table(dat$pre)
table(dat$during)
table(dat$post)
table(dat$sound)


## convert behvaior into long format 

dat_long = gather(dat, sound_time, behavior, pre:post, factor_key = T)

###total counts of different types of behavior #########################################################################################

behav_count = dat_long %>% group_by(sound, species, sound_time, behavior) %>% count()

behav_prop_sound= behav_count %>% 
  group_by(sound) %>% 
  mutate(behav_prop = 
           paste0(round(n/sum(n)*100,2)))

behav_prop_species= behav_count %>% 
  group_by(species) %>% 
  mutate(behav_prop = 
           paste0(round(n/sum(n)*100,2)))

behav_prop_sound_species= behav_count %>% 
  group_by(sound, species) %>% 
  mutate(behav_prop = 
           paste0(round(n/sum(n)*100,2)))

behav_prop_soundtime_species= behav_count %>% 
  group_by(sound, sound_time, species) %>% 
  mutate(behav_prop = 
           paste0(round(n/sum(n)*100,2)))

###plot #######################################################################################

## plot overall behavior proportions per site #####################################
behav_prop_soundtime_species %>% filter(!is.na(behavior)) %>% 
  ggplot(aes(x = behavior, y = behav_prop, color = species)) +
  geom_bar() + 
  labs(x = "Behavior Type", y = "Proportion", fill = "Species") + scale_color_brewer(palette="Set1")


############################################################################
##behavior by species and sound

behav_prop_soundtime_species %>% 
  filter(!is.na(behavior)) %>% 
  filter(!is.na(species)) %>% 
  ggplot(aes(x = species,fill = behavior)) + 
  geom_bar(position = "fill") + 
  labs(x = "Species", y = "Proportion of videos", 
       title = "Behavior state by species", fill = "Behavior type")

behav_prop_soundtime_species %>%
  filter(behavior != "na") %>% 
  filter(species != "na") %>%
  filter(species != "wind triggered") %>%
  filter(species != "unk") %>% 
  filter(species != "starling") %>% 
  ggplot(aes(x = species,fill = behavior)) + #change x= based on if I want to use original or updated sighting quant
  geom_bar(position = "fill") + facet_grid(cols = vars(sound)) +
  labs(x = "Species", y = "Behavior Proportion", 
       fill = "Behavior Type")+
  theme(axis.text.x = element_text(angle=90))


behav_prop_soundtime_species %>%
  filter(behavior != "na") %>% 
  filter(species == "cardinal") %>%
  ggplot(aes(x = species,fill = behavior)) + #change x= based on if I want to use original or updated sighting quant
  geom_bar(position = "fill") + facet_grid(cols = vars(sound)) +
  labs(x = "Species", y = "Behavior Proportion", 
       fill = "Behavior Type")+
  theme(axis.text.x = element_text(angle=90))



