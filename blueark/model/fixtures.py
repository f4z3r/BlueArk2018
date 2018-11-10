import blueark.model.entities as entities

src = entities.Source(100, False)
srcToTank = entities.Pipe(src, 300, 0, 300)
tank = entities.Tank([srcToTank], 250000, 10000)
left = entities.Pipe(tank, 300, 0, 300)
consumer1 = entities.Consumer([left], 200)
right = entities.Pipe(tank, 200, 0.5, 300)
consumer2 = entities.Consumer([left, right], 150)

graph = consumer2

