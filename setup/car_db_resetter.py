from car_database import CarDatabase
import asyncio

# import os
#
# file_path = 'Users\Debro\PycharmProjects\Dragon\car_data.db'
#
# if os.path.exists(file_path):
#     os.remove(file_path)
# else:
#     print(f"The file '{file_path}' does not exist.")

database = CarDatabase()


async def update():
    await database.create_car_database()
    await database.add_car('Lamborghini Revuelto',
                            '1195082451630948484/1.png?ex=65b2b244&is=65a03d44&hm=eda81527c55aec2538b86dea8a86baf7cbca60010293f7e58c9fc322519b3db1&',
                            'Arancio Borealis', 'Lamborghini', 'Revuelto',
                            2024, 85.69, 608400, 'A', 'Supercar', 40,
                            217.5, 2.4, 1001, 535, 3907,
                            350, 2.5, 1015, 725, 1772)
    await database.add_car('Ford Mustang EcoBoost Fastback',
                              '1195068102359134258/4.png?ex=65b2a4e6&is=65a02fe6&hm=43ea2c8575c57d13ce6dc2a8a4457fad4c4ae02ac962a8394ac05980dbf0f583&',
                              'Oxford White', 'Ford', 'Mustang EcoBoost Fastback',
                              2024, 31.68, 31000, 'D', 'Sports Car', 10,
                              145, 4.5, 315, 350, 3588,
                              233, 4.7, 319, 475, 1627)
    await database.add_car('Ferrari SF90 Stradale',
                          '1194725188902862859/2.png?ex=65b16589&is=659ef089&hm=effe81fbf5e4828939de2752ca5af1d0fd95bfb7b280d0adfa6b31ca820c7220&',
                          'Rosso Corsa', 'Ferrari', 'SF90 Stradale',
                          2019, 83.90, 524900, 'A', 'Supercar', 40,
                          211, 2.4, 986, 590, 3461,
                          340, 2.5, 1000, 800, 1570)
    await database.add_car('Chevrolet Camaro 1LS',
                          '1195094252485607565/9.png?ex=65b2bd41&is=65a04841&hm=5fa679e87997e3e723bc1e3d6532c81fab1d0d02453b17051fe307a74a6c98a8&',
                          'Summit White', 'Chevrolet', 'Camaro 1LS',
                          2019, 22.59, 26400, 'D', 'Sports Car', 10,
                          149, 5.4, 275, 295, 3351,
                          240, 5.6, 279, 400, 1520)
    await database.add_car('Aston Martin DB12',
                          '1195111385605095444/10.png?ex=65b2cd36&is=65a05836&hm=dea2ed4a4c088630a89a3725ff25dbd4382f5c80559347b1d8b9ed2c3cd6eb65&',
                          'Iridescent Emerald', 'Aston Martin', 'DB12',
                          2024, 70.86, 248100, 'B', 'Supercar', 25,
                          202, 3.4, 671, 590, 3715,
                          325, 3.5, 680, 800, 1685)
    await database.add_car('Audi R8 GT',
                          '1195261544452337704/11.png?ex=65b3590f&is=65a0e40f&hm=6bb5a051f686db94160379c46caac98d4ab68fcd4dc7c7c186e2bae853db505b&',
                          'Suzuka Gray', 'Audi', 'R8 GT',
                          2023, 72.61, 249900, 'B', 'Supercar', 25,
                          199, 3.2, 602, 413, 3516,
                          320, 3.3, 610, 560, 1595)
    await database.add_car('Honda Civic Type R',
                          '',
                          '', 'Honda', 'Civic Type R',
                          2022, 35.19, 44900, 'C', 'Hatchback', 15,
                          170, 4.9, 602, 413, 3516,
                          274, 5.1, 610, 560, 1595)

asyncio.run(update())
