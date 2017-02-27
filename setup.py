from setuptools import (
    find_packages,
    setup,
)


setup(
    name='papikaai',
    version='0.0.1',
    description="Artificial intelligence with Papika",
    url='https://github.com/kennydo/papika-ai',
    author='Kenny Do',
    author_email='chinesedewey@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
    packages=find_packages(exclude=['tests']),
    package_data={
    },
    include_package_Data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
        ],
        'papika_ai.action_handlers': [
            'input.unknown = papikaai.action_handlers.fallback:Fallback',
            'lights.set_room_brightness = papikaai.action_handlers.set_room_brightness:SetRoomBrightness',
            'lights.turn_off_room_lights = papikaai.action_handlers.turn_off_room_lights:TurnOffRoomLights',
            'lights.turn_on_room_lights = papikaai.action_handlers.turn_on_room_lights:TurnOnRoomLights',
        ],
    },
)
