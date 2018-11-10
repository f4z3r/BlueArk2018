import blueark.model.entities as entities

consumer1 = entities.Consumer(200)
consumer2 = entities.Consumer(150)
right = entities.Pipe(consumer2, 200, 0.5, 300)
left = entities.Pipe(consumer2, 300, 0, 300)
tank = entities.Tank([left, right], 250000, 10000)
tankToSrc = entities.Pipe(tank, 300, 0, 300)
src = entities.Source(tankToSrc, 100, False)

graph = src
