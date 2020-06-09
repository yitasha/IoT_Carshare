from pushbullet import Pushbullet

api_key = "o.aEjo2hFS6HFhr2CUtS39MIrNQJhlxngY"
pb = Pushbullet(api_key)

pb.push_note("This is headers", "This is message body")
print(pb.devices)