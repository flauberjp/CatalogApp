from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import db_string, Category, Item

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()

# Create category Soccer
soccer_category = Category(name="Soccer")
session.add(soccer_category)
session.commit()

# Create Item "Two shinguards" for category "Soccer"
two_shinguards_item = Item(name="Two shinguards",
                           description="A shin guard or shin pad is a piece \
                           of equipment worn on the front of a player's shin \
                           to protect them from injury.",
                           category=soccer_category)

session.add(two_shinguards_item)
session.commit()

# Create category Snowboarding
snowboarding_category = Category(name="Snowboarding")
session.add(snowboarding_category)
session.commit()

# Create Item Snowboard for category Snowboarding
snowboard_item = Item(name="Snowboard",
                      description="Best for any terrain and conditions. \
                      All-mountain snowboards perform anyware on a mountain \
                      - groomed runs, backcountry, even park and pipe. They \
                      may be directional (meaning downhill only) or twin-tip \
                      (for riding switch, meaning either direction). Most \
                      boarders ride all-mountain boards. Because of their \
                      versatility, all-mountain boards are good for \
                      beginners who are still learning what terrain they \
                      like.", category=snowboarding_category)

session.add(snowboard_item)
session.commit()

# Create Item Goggles for category Snowboarding
goggles_item = Item(name="Goggles",
                    description="A nice pair of snowboard goggles can be the \
                    difference between a fun day on the slopes, and heading \
                    in to the lodge early because you can’t see. On stormy \
                    days, the snow and cloudy grey skies can blend into one \
                    another, making it nearly impossible to see where you’re \
                    riding.", category=snowboarding_category)

session.add(goggles_item)
session.commit()

# Create category
category = Category(name="Basketball")
session.add(category)
session.commit()

# Create category
category = Category(name="Baseball")
session.add(category)
session.commit()

# Create category
category = Category(name="Frisbee")
session.add(category)
session.commit()

# Create category
category = Category(name="Rock Climbing")
session.add(category)
session.commit()

# Create category
category = Category(name="Foosball")
session.add(category)
session.commit()

# Create category
category = Category(name="Hockey")
session.add(category)
session.commit()

print("added categories and items!")
