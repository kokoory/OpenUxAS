"""Chapters 4-6: Installation, Task Types, Configuration"""

def write_chapter4(pdf):
    """Chapter 4: Installation"""
    pdf.ch('\uc124\uce58 \ubc0f \ube4c\ub4dc',
           'Installation and Build')

    pdf.sec('\uc2dc\uc2a4\ud15c \uc694\uad6c\uc0ac\ud56d')
    pdf.p('\ub2e4\uc74c \ud658\uacbd\uc774 \ud544\uc694\ud569\ub2c8\ub2e4:')
    pdf.tbl(
        ['\ud56d\ubaa9', '\uc694\uad6c\uc0ac\ud56d', '\ube44\uace0'],
        [
            ['\uc6b4\uc601\uccb4\uc81c', 'Ubuntu 22.04 / 20.04', 'Linux \uad8c\uc7a5'],
            ['\ubc84\uc804 \uad00\ub9ac', 'git', '\uc18c\uc2a4 \ucf54\ub4dc \ud074\ub860'],
            ['\ube4c\ub4dc \ub3c4\uad6c', '\uc790\ub3d9 \uc124\uce58 (anod)', 'Meson + Ninja'],
            ['Java', 'JDK 8+', 'OpenAMASE \uc2e4\ud589\uc6a9'],
            ['\ub514\uc2a4\ud06c', '\ucd5c\uc18c 10GB', '\uc758\uc874\uc131 \ud3ec\ud568'],
        ],
        [30, 55, 100]
    )

    pdf.sec('\uc124\uce58 \uc808\ucc28')
    pdf.subsec('Step 1: \uc18c\uc2a4 \ucf54\ub4dc \ud074\ub860')
    pdf.code('$ git clone https://github.com/afrl-rq/OpenUxAS\n$ cd OpenUxAS', '\uc800\uc7a5\uc18c \ud074\ub860')
    pdf.p('GitHub\uc5d0\uc11c OpenUxAS \uc800\uc7a5\uc18c\ub97c \ud074\ub860\ud569\ub2c8\ub2e4. \ubaa8\ub4e0 \uc18c\uc2a4 \ucf54\ub4dc\uc640 \uc608\uc81c\uac00 \ud3ec\ud568\ub418\uc5b4 \uc788\uc2b5\ub2c8\ub2e4.')

    pdf.subsec('Step 2: OpenUxAS \ube4c\ub4dc')
    pdf.code('$ ./anod build uxas', 'UxAS \ube4c\ub4dc')
    pdf.p('anod \uba85\ub839\uc740 \ubaa8\ub4e0 \uc758\uc874\uc131(ZeroMQ, Boost, \ub4f1)\uc744 \uc790\ub3d9\uc73c\ub85c \ub2e4\uc6b4\ub85c\ub4dc\ud558\uace0 \ube4c\ub4dc\ud569\ub2c8\ub2e4. \uccab \ube4c\ub4dc\ub294 \uc0c1\ub2f9\ud55c \uc2dc\uac04\uc774 \uc18c\uc694\ub420 \uc218 \uc788\uc2b5\ub2c8\ub2e4.')

    pdf.subsec('Step 3: OpenAMASE \ube4c\ub4dc')
    pdf.code('$ ./anod build amase', 'AMASE \uc2dc\ubbac\ub808\uc774\ud130 \ube4c\ub4dc')
    pdf.p('OpenAMASE\ub294 UAV \uc2dc\ubbac\ub808\uc774\ud130\ub85c, \uc2e4\uc81c \ube44\ud589\uccb4 \uc5c6\uc774 OpenUxAS\ub97c \ud14c\uc2a4\ud2b8\ud560 \uc218 \uc788\uac8c \ud574\uc90d\ub2c8\ub2e4.')

    pdf.subsec('Step 4: \uc608\uc81c \uc2e4\ud589 \ud655\uc778')
    pdf.code('$ ./run-example 01_HelloWorld', '\uccab \ubc88\uc9f8 \uc608\uc81c \uc2e4\ud589')
    pdf.p('Hello World \uc608\uc81c\uac00 \uc815\uc0c1\uc801\uc73c\ub85c \uc2e4\ud589\ub418\uba74 \uc124\uce58\uac00 \uc644\ub8cc\ub41c \uac83\uc785\ub2c8\ub2e4.')

    pdf.sec('\uc99d\ubd84 \ube4c\ub4dc (Incremental Build)')
    pdf.p('anod\ub85c \uccab \ube4c\ub4dc \ud6c4, \ucf54\ub4dc\ub97c \uc218\uc815\ud558\uba74 make\ub85c \ube60\ub974\uac8c \uc7ac\ube4c\ub4dc\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4:')
    pdf.code('$ make -j all', '\uc99d\ubd84 \ube4c\ub4dc')
    pdf.p('run-example\uacfc tests/run-tests \uc2a4\ud06c\ub9bd\ud2b8\ub294 make\ub85c \ube4c\ub4dc\ub41c \ubc14\uc774\ub108\ub9ac\ub97c \uc790\ub3d9\uc73c\ub85c \uc0ac\uc6a9\ud569\ub2c8\ub2e4.')

    pdf.sec('\ud14c\uc2a4\ud2b8 \uc2e4\ud589')
    pdf.code('$ cd tests/cpp\n$ ./run-tests', 'C++ \ud14c\uc2a4\ud2b8 \uc2e4\ud589')
    pdf.p('C++ \ub2e8\uc704 \ud14c\uc2a4\ud2b8\ub97c \uc2e4\ud589\ud558\uc5ec \ube4c\ub4dc\uac00 \uc815\uc0c1\uc801\uc778\uc9c0 \ud655\uc778\ud569\ub2c8\ub2e4.')

    pdf.sec('\ub514\ub809\ud1a0\ub9ac \uad6c\uc870')
    pdf.code('''OpenUxAS/
\u251c\u2500\u2500 src/cpp/
\u2502   \u251c\u2500\u2500 Services/        # \ud575\uc2ec \uc11c\ube44\uc2a4 (\uc57d 30\uac1c)
\u2502   \u251c\u2500\u2500 Tasks/           # \ud0dc\uc2a4\ud06c \uc11c\ube44\uc2a4 (\uc57d 15\uac1c)
\u2502   \u251c\u2500\u2500 Communications/  # \ud1b5\uc2e0 \uacc4\uce35 (LMCP, ZeroMQ)
\u2502   \u251c\u2500\u2500 Utilities/       # \uc720\ud2f8\ub9ac\ud2f0 (FlatEarth, UnitConversion)
\u2502   \u2514\u2500\u2500 DPSS/            # \ub3d9\uc801 \ub458\ub808 \uac10\uc2dc \uc2dc\uc2a4\ud15c
\u251c\u2500\u2500 examples/
\u2502   \u251c\u2500\u2500 01_HelloWorld/       # \uae30\ubcf8 \uc608\uc81c
\u2502   \u251c\u2500\u2500 02_Example_Waterway/ # \uc218\ub85c \ud0d0\uc0c9
\u2502   \u251c\u2500\u2500 03_DistributedCoop/  # \ubd84\uc0b0 \ud611\ub3d9
\u2502   \u251c\u2500\u2500 05_AssignTasks/      # \uc784\ubb34 \ud560\ub2f9
\u2502   \u2514\u2500\u2500 99_Tasks/            # \uac1c\ubcc4 \ud0dc\uc2a4\ud06c \uc608\uc81c
\u251c\u2500\u2500 mdms/                # LMCP \uba54\uc2dc\uc9c0 \uc815\uc758 (XML)
\u251c\u2500\u2500 tests/               # \ud14c\uc2a4\ud2b8
\u2514\u2500\u2500 resources/           # \ubb38\uc11c \ube4c\ub4dc \ub3c4\uad6c''', '\uc8fc\uc694 \ub514\ub809\ud1a0\ub9ac \uad6c\uc870')


def write_chapter5(pdf):
    """Chapter 5: Task Types"""
    pdf.ch('\ud0dc\uc2a4\ud06c \uc720\ud615 \uc0c1\uc138',
           'Task Types in Detail')

    pdf.sec('\uc601\uc5ed \ud0d0\uc0c9 \ud0dc\uc2a4\ud06c (Area Search Tasks)')

    pdf.subsec('AngledAreaSearchTask')
    pdf.p('\uc9c0\uc815\ub41c \uac01\ub3c4\ub85c \ub2e4\uac01\ud615 \uc601\uc5ed\uc744 \ud0d0\uc0c9\ud558\ub294 \ud0dc\uc2a4\ud06c\uc785\ub2c8\ub2e4. \uac00\uc7a5 \ub9ce\uc774 \uc0ac\uc6a9\ub418\ub294 \uc601\uc5ed \ud0d0\uc0c9 \ubc29\uc2dd\uc785\ub2c8\ub2e4.')
    pdf.p('\uc8fc\uc694 \ud30c\ub77c\ubbf8\ud130:')
    pdf.bullets([
        'SearchAreaID: \ud0d0\uc0c9\ud560 \uc601\uc5ed\uc758 ID (AreaOfInterest \ucc38\uc870)',
        'SweepAngle: \ud0d0\uc0c9 \ubc29\ud5a5 \uac01\ub3c4 (0=\ubd81\ucabd, 90=\ub3d9\ucabd)',
        'GroundSampleDistance: \uc694\uad6c\ub418\ub294 \uc9c0\uc0c1 \ud574\uc0c1\ub3c4 (m/pixel)',
    ])
    pdf.code('''<AngledAreaSearchTask Series="uxas.messages.task">
    <TaskID>100</TaskID>
    <Label>AreaSearch_Task</Label>
    <SearchAreaID>1</SearchAreaID>
    <SweepAngle>45</SweepAngle>
    <DesiredWavelengthBands>
        <WavelengthBand>EO</WavelengthBand>
    </DesiredWavelengthBands>
    <GroundSampleDistance>0.5</GroundSampleDistance>
</AngledAreaSearchTask>''', 'AngledAreaSearchTask XML \uc608\uc2dc')
    pdf.p('\ub3d9\uc791 \ubc29\uc2dd:')
    pdf.p('1) \uc601\uc5ed \uacbd\uacc4\ub97c SweepAngle \ubc29\ud5a5\uc73c\ub85c \ud68c\uc804\ud558\uc5ec \uc815\ub82c\ud569\ub2c8\ub2e4.')
    pdf.p('2) \uc13c\uc11c \ud48b\ud504\ub9b0\ud2b8 \ud3ed * 0.9 \uac04\uaca9\uc73c\ub85c \ud3c9\ud589 \ub808\uc778\uc744 \uc0dd\uc131\ud569\ub2c8\ub2e4.')
    pdf.p('3) \uac01 \ub808\uc778\uacfc \uc601\uc5ed \uacbd\uacc4\uc758 \uad50\ucc28\uc810\uc744 \uacc4\uc0b0\ud558\uc5ec \uc6e8\uc774\ud3ec\uc778\ud2b8\ub97c \uc0dd\uc131\ud569\ub2c8\ub2e4.')
    pdf.p('4) 4\uac1c \ucf54\ub108\uc5d0\uc11c \uc2dc\uc791\ud558\ub294 \uc635\uc158\uc744 \uc0dd\uc131\ud558\uc5ec \ucd5c\uc801\uc758 \uc2dc\uc791 \uc704\uce58\ub97c \uc120\ud0dd\ud569\ub2c8\ub2e4.')

    pdf.subsec('CmasiAreaSearchTask')
    pdf.p('CMASI(Common Mission Automation Services Interface) \ud45c\uc900 \uc601\uc5ed \ud0d0\uc0c9 \ud0dc\uc2a4\ud06c\uc785\ub2c8\ub2e4. \ub2e4\uc591\ud55c \uc601\uc5ed \ud615\ud0dc(\ub2e4\uac01\ud615, \uc6d0\ud615, \uc0ac\uac01\ud615)\ub97c \uc9c0\uc6d0\ud558\uba70, \ubcf5\uc218\uc758 \uc2dc\uc57c\uac01(ViewAngle) \uc870\ud569\uc73c\ub85c \ud0d0\uc0c9 \uc635\uc158\uc744 \uc0dd\uc131\ud569\ub2c8\ub2e4.')
    pdf.code('''<AreaSearchTask Series="CMASI">
    <TaskID>100</TaskID>
    <Label>Circular_Search</Label>
    <SearchArea>
        <Circle>
            <CenterPoint>
                <Location3D Latitude="45.317" Longitude="-120.913"
                            Altitude="0" AltitudeType="MSL"/>
            </CenterPoint>
            <Radius>2000.0</Radius>
        </Circle>
    </SearchArea>
    <ViewAngleList>
        <Wedge AzimuthCenterline="0" VerticalCenterline="-60"
               AzimuthExtent="360" VerticalExtent="30"/>
    </ViewAngleList>
    <DesiredWavelengthBands>EO</DesiredWavelengthBands>
</AreaSearchTask>''', 'CmasiAreaSearchTask XML \uc608\uc2dc (\uc6d0\ud615 \uc601\uc5ed)')

    pdf.subsec('PatternSearchTask')
    pdf.p('\ud2b9\uc815 \uc9c0\uc810 \uc911\uc2ec\uc73c\ub85c \ud328\ud134 \ud0d0\uc0c9\uc744 \uc218\ud589\ud569\ub2c8\ub2e4. 3\uac00\uc9c0 \ud328\ud134\uc744 \uc9c0\uc6d0:')
    pdf.bullets([
        'Spiral: \ub098\uc120\ud615\uc73c\ub85c \uc911\uc2ec\uc5d0\uc11c \ud655\uc7a5\ud558\uba70 \ud0d0\uc0c9',
        'Sector: \ubd80\ucc44\uaf34 \ud615\ud0dc\ub85c \uad6c\uc5ed\uc744 \ub098\ub204\uc5b4 \ud0d0\uc0c9',
        'Sweep: \ub2e8\uc21c \uc2a4\uc704\ud551 \ud0d0\uc0c9',
    ])

    pdf.sec('\ub77c\uc778 \ud0d0\uc0c9 \ud0dc\uc2a4\ud06c (Line Search Tasks)')
    pdf.subsec('CmasiLineSearchTask')
    pdf.p('\ub3c4\ub85c, \ud574\uc548\uc120, \uac15 \ub4f1\uc758 \ub77c\uc778\uc744 \ub530\ub77c \uce74\uba54\ub77c\ub85c \ud0d0\uc0c9\ud558\ub294 \ud0dc\uc2a4\ud06c\uc785\ub2c8\ub2e4. \uc9c0\uc815\ub41c \uac01\ub3c4\uc5d0\uc11c \ub77c\uc778\uc744 \ucd2c\uc601\ud558\ub294 \uc6e8\uc774\ud3ec\uc778\ud2b8\ub97c \uc790\ub3d9 \uc0dd\uc131\ud569\ub2c8\ub2e4.')
    pdf.p('\uc608\ub97c \ub4e4\uc5b4 \uc218\ub85c \ud0d0\uc0c9(Waterway Search) \uc608\uc81c\uc5d0\uc11c \ud65c\uc6a9\ub429\ub2c8\ub2e4. UAV\uac00 \uc218\ub85c \uc606\uc744 \ube44\ud589\ud558\uba74\uc11c \uce74\uba54\ub77c\ub97c \uc218\ub85c \ubc29\ud5a5\uc73c\ub85c \ud5a5\ud558\uc5ec \uc5f0\uc18d \ucd2c\uc601\ud569\ub2c8\ub2e4.')

    pdf.sec('\uc9c0\uc810 \ud0d0\uc0c9 \ud0dc\uc2a4\ud06c (Point Search Tasks)')
    pdf.subsec('CmasiPointSearchTask')
    pdf.p('\ud2b9\uc815 \uc9c0\uc810\uc744 \uac10\uc2dc\ud558\ub294 \ud0dc\uc2a4\ud06c\uc785\ub2c8\ub2e4. UAV\uac00 \ud574\ub2f9 \uc9c0\uc810 \uc8fc\uc704\ub97c \ub85c\uc774\ud130(Loiter)\ud558\uba74\uc11c \uce74\uba54\ub77c\ub85c \uac10\uc2dc\ud569\ub2c8\ub2e4.')

    pdf.sec('\ud611\ub3d9 \uc784\ubb34 \ud0dc\uc2a4\ud06c (Cooperative Tasks)')
    pdf.tbl(
        ['\ud0dc\uc2a4\ud06c', '\uc124\uba85', '\ucc28\ub7c9 \uc218'],
        [
            ['WatchTask', '\ud2b9\uc815 \uc9c0\uc810 \uc9c0\uc18d \uac10\uc2dc', '1\ub300'],
            ['MultiVehicleWatchTask', '\ub2e4\uc218 UAV\uac00 \uad50\ub300\ub85c \uac10\uc2dc', '2\ub300+'],
            ['BlockadeTask', '\uc601\uc5ed \uc9c4\uc785 \ucc28\ub2e8', '1\ub300+'],
            ['CordonTask', '\ub458\ub808 \ubd09\uc1c4/\uac10\uc2dc', '1\ub300+'],
            ['EscortTask', '\ub2e4\ub978 \ucc28\ub7c9 \ud638\uc704', '1\ub300'],
            ['CommRelayTask', 'UAV\uac04 \ud1b5\uc2e0 \uc911\uacc4', '1\ub300'],
            ['RendezvousTask', '\uc9c0\uc815 \uc9c0\uc810\uc5d0\uc11c \ud569\ub958', '2\ub300+'],
            ['LoiterTask', '\uc9c0\uc810 \uc8fc\uc704 \uc21c\ud68c \ube44\ud589', '1\ub300'],
            ['OverwatchTask', '\ub192\uc740 \uc704\uce58\uc5d0\uc11c \uac10\uc2dc', '1\ub300'],
        ],
        [55, 80, 50]
    )


def write_chapter6(pdf):
    """Chapter 6: Configuration"""
    pdf.ch('XML \uc124\uc815 \uc0c1\uc138',
           'XML Configuration in Detail')

    pdf.sec('\uc124\uc815 \ud30c\uc77c \uad6c\uc870')
    pdf.p('OpenUxAS\ub294 XML \ud30c\uc77c\ub85c \uc2dc\uc2a4\ud15c\uc744 \uc124\uc815\ud569\ub2c8\ub2e4. \ub450 \uc885\ub958\uc758 \uc124\uc815 \ud30c\uc77c\uc774 \uc788\uc2b5\ub2c8\ub2e4:')
    pdf.bullets([
        'config.yaml: \uc608\uc81c \uc2e4\ud589 \uc124\uc815 (\uc5b4\ub5a4 \uc2dc\ub098\ub9ac\uc624\uc640 UxAS \uc124\uc815\uc744 \uc0ac\uc6a9\ud560\uc9c0)',
        'cfg_*.xml: UxAS \uc11c\ube44\uc2a4 \uc124\uc815 (\uc5b4\ub5a4 \uc11c\ube44\uc2a4\ub97c \uc2e4\ud589\ud558\uace0 \uc5b4\ub5a4 \uba54\uc2dc\uc9c0\ub97c \uc804\uc1a1\ud560\uc9c0)',
    ])

    pdf.subsec('config.yaml \ud615\uc2dd')
    pdf.code('''amase:
  scenario: Scenario_WaterwaySearch.xml   # AMASE \uc2dc\ub098\ub9ac\uc624 \ud30c\uc77c

uxas:
  config: cfg_WaterwaySearch.xml          # UxAS \uc124\uc815 \ud30c\uc77c
  rundir: RUNDIR_WaterwaySearch           # \uc2e4\ud589 \uacb0\uacfc \ub514\ub809\ud1a0\ub9ac''', 'config.yaml \uc608\uc2dc')

    pdf.subsec('cfg_*.xml \uae30\ubcf8 \uad6c\uc870')
    pdf.code('''<?xml version="1.0" encoding="UTF-8"?>
<UxAS FormatVersion="1.0" EntityID="100"
      EntityType="Aircraft">

  <!-- \ud1b5\uc2e0 \ube0c\ub9ac\uc9c0 \uc124\uc815 -->
  <Bridge Type="LmcpObjectNetworkTcpBridge"
          TcpAddress="tcp://127.0.0.1:5555" Server="TRUE"/>

  <!-- \uc11c\ube44\uc2a4 \uc124\uc815 -->
  <Service Type="AutomationRequestValidatorService"/>
  <Service Type="RouteAggregatorService"/>
  <Service Type="RoutePlannerVisibilityService"/>
  <Service Type="AssignmentTreeBranchBoundService"/>
  <Service Type="PlanBuilderService"/>
  <Service Type="TaskManagerService"/>
  <Service Type="WaypointPlanManagerService"/>
  <Service Type="SensorManagerService"/>

  <!-- \ucd08\uae30 \uba54\uc2dc\uc9c0 (\ucc28\ub7c9, \uc784\ubb34, \uc601\uc5ed \uc815\uc758) -->
  <SendMessagesService>
    <!-- \uc5ec\uae30\uc5d0 LMCP \uba54\uc2dc\uc9c0 XML\uc774 \ub4e4\uc5b4\uac10 -->
  </SendMessagesService>
</UxAS>''', 'cfg_*.xml \uae30\ubcf8 \uad6c\uc870')

    pdf.sec('UAV \uc124\uc815 (AirVehicleConfiguration)')
    pdf.code('''<AirVehicleConfiguration Series="CMASI">
  <ID>400</ID>
  <Label>UAV_400</Label>
  <MinimumSpeed>15.0</MinimumSpeed>
  <MaximumSpeed>35.0</MaximumSpeed>
  <NominalSpeed>22.0</NominalSpeed>
  <NominalAltitude>700.0</NominalAltitude>
  <NominalAltitudeType>MSL</NominalAltitudeType>
  <MinimumAltitude>50.0</MinimumAltitude>
  <MaximumAltitude>1500.0</MaximumAltitude>
  <PayloadConfigurationList>
    <CameraConfiguration>
      <PayloadID>1</PayloadID>
      <SupportedWavelengthBand>EO</SupportedWavelengthBand>
      <MaxHorizontalFieldOfView>45.0</MaxHorizontalFieldOfView>
      <MinHorizontalFieldOfView>2.0</MinHorizontalFieldOfView>
      <VideoStreamHorizontalResolution>1920</VideoStreamHorizontalResolution>
      <VideoStreamVerticalResolution>1080</VideoStreamVerticalResolution>
    </CameraConfiguration>
  </PayloadConfigurationList>
  <NominalFlightProfile>
    <FlightProfile Name="Nominal" Airspeed="22.0"
                   EnergyRate="0.005"/>
  </NominalFlightProfile>
</AirVehicleConfiguration>''', 'UAV \uc124\uc815 XML \uc608\uc2dc')

    pdf.p('\uc8fc\uc694 \ud30c\ub77c\ubbf8\ud130 \uc124\uba85:')
    pdf.tbl(
        ['\ud30c\ub77c\ubbf8\ud130', '\ub2e8\uc704', '\uc124\uba85'],
        [
            ['NominalSpeed', 'm/s', '\uae30\ubcf8 \ube44\ud589 \uc18d\ub3c4'],
            ['NominalAltitude', 'm', '\uae30\ubcf8 \ube44\ud589 \uace0\ub3c4'],
            ['MaxHorizontalFOV', 'degree', '\uce74\uba54\ub77c \ucd5c\ub300 \uc218\ud3c9 \uc2dc\uc57c\uac01'],
            ['MinHorizontalFOV', 'degree', '\uce74\uba54\ub77c \ucd5c\uc18c \uc218\ud3c9 \uc2dc\uc57c\uac01'],
            ['Resolution', 'pixel', '\uce74\uba54\ub77c \ud574\uc0c1\ub3c4 (H x V)'],
        ],
        [50, 25, 110]
    )

    pdf.sec('\uc601\uc5ed \uc815\uc758 (AreaOfInterest)')
    pdf.code('''<AreaOfInterest Series="CMASI">
  <AreaID>1</AreaID>
  <Area>
    <Polygon>
      <BoundaryPoints>
        <Location3D Latitude="45.3171" Longitude="-120.9139"
                    Altitude="0" AltitudeType="MSL"/>
        <Location3D Latitude="45.3171" Longitude="-120.8000"
                    Altitude="0" AltitudeType="MSL"/>
        <Location3D Latitude="45.2500" Longitude="-120.8000"
                    Altitude="0" AltitudeType="MSL"/>
        <Location3D Latitude="45.2500" Longitude="-120.9139"
                    Altitude="0" AltitudeType="MSL"/>
      </BoundaryPoints>
    </Polygon>
  </Area>
</AreaOfInterest>''', '\ub2e4\uac01\ud615 \uc601\uc5ed \uc815\uc758 \uc608\uc2dc')

    pdf.sec('\uc6b4\uc6a9 \uc601\uc5ed \uc124\uc815')
    pdf.p('KeepInZone(\ube44\ud589 \ud5c8\uc6a9)\uacfc KeepOutZone(\ube44\ud589 \uae08\uc9c0)\uc73c\ub85c \uc6b4\uc6a9 \uc601\uc5ed\uc744 \uc815\uc758\ud569\ub2c8\ub2e4:')
    pdf.code('''<!-- \ube44\ud589 \ud5c8\uc6a9 \uc601\uc5ed -->
<KeepInZone Series="CMASI">
  <ZoneID>1</ZoneID>
  <Boundary>
    <Polygon>
      <BoundaryPoints>
        <!-- \ud5c8\uc6a9 \uc601\uc5ed \uacbd\uacc4\uc810 -->
      </BoundaryPoints>
    </Polygon>
  </Boundary>
  <MinAltitude>0</MinAltitude>
  <MaxAltitude>10000</MaxAltitude>
</KeepInZone>

<!-- \ube44\ud589 \uae08\uc9c0 \uc601\uc5ed -->
<KeepOutZone Series="CMASI">
  <ZoneID>10</ZoneID>
  <Boundary>
    <Polygon>
      <BoundaryPoints>
        <!-- \uae08\uc9c0 \uc601\uc5ed \uacbd\uacc4\uc810 -->
      </BoundaryPoints>
    </Polygon>
  </Boundary>
</KeepOutZone>

<!-- \uc6b4\uc6a9 \uc601\uc5ed = \ud5c8\uc6a9 - \uae08\uc9c0 -->
<OperatingRegion Series="CMASI">
  <ID>100</ID>
  <KeepInAreaList><uint64>1</uint64></KeepInAreaList>
  <KeepOutAreaList><uint64>10</uint64></KeepOutAreaList>
</OperatingRegion>''', '\uc6b4\uc6a9 \uc601\uc5ed \uc124\uc815 XML')
