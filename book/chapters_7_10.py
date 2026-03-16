"""Chapters 7-10: Examples, Multi-Vehicle, Results, Advanced"""

def write_chapter7(pdf):
    """Chapter 7: Running Examples"""
    pdf.ch('\uc608\uc81c \uc2e4\uc2b5',
           'Hands-on Examples')

    pdf.sec('\uc608\uc81c \ubaa9\ub85d')
    pdf.tbl(
        ['\uc608\uc81c', '\uc124\uba85', '\ub09c\uc774\ub3c4'],
        [
            ['01_HelloWorld', '\uae30\ubcf8 \uc2e4\ud589 \ud14c\uc2a4\ud2b8', '\u2605'],
            ['02_WaterwaySearch', '\uc218\ub85c \ud0d0\uc0c9 (1\ub300)', '\u2605\u2605'],
            ['02b_Double_Waterway', '\uc218\ub85c \ud0d0\uc0c9 (2\ub300)', '\u2605\u2605\u2605'],
            ['03_DistributedCoop', '\ubd84\uc0b0 \ud611\ub3d9', '\u2605\u2605\u2605'],
            ['05_AssignTasks', '\uc784\ubb34 \ud560\ub2f9', '\u2605\u2605'],
            ['99_Tasks/*', '\uac1c\ubcc4 \ud0dc\uc2a4\ud06c \uc608\uc81c', '\u2605\u2605'],
        ],
        [55, 80, 50]
    )

    pdf.sec('\uc608\uc81c 1: HelloWorld')
    pdf.p('\uac00\uc7a5 \uae30\ubcf8\uc801\uc778 \uc608\uc81c\ub85c, OpenUxAS\uac00 \uc815\uc0c1\uc801\uc73c\ub85c \ube4c\ub4dc\ub418\uc5c8\ub294\uc9c0 \ud655\uc778\ud569\ub2c8\ub2e4.')
    pdf.code('$ ./run-example 01_HelloWorld', '\uc2e4\ud589 \uba85\ub839')
    pdf.p('UxAS \ud504\ub85c\uc138\uc2a4\uac00 \uc2dc\uc791\ub418\uace0 \uae30\ubcf8 \uc11c\ube44\uc2a4\uac00 \ucd08\uae30\ud654\ub418\ub294 \uac83\uc744 \ud655\uc778\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.')

    pdf.sec('\uc608\uc81c 2: \uc218\ub85c \ud0d0\uc0c9 (Waterway Search)')
    pdf.p('\uac00\uc7a5 \ub300\ud45c\uc801\uc778 \uc608\uc81c\ub85c, 1\ub300\uc758 UAV\uac00 \uc218\ub85c\ub97c \ub530\ub77c \uce74\uba54\ub77c \uac10\uc2dc\ub97c \uc218\ud589\ud569\ub2c8\ub2e4.')
    pdf.code('$ ./run-example 02_Example_WaterwaySearch', '\uc2e4\ud589 \uba85\ub839')

    pdf.subsec('\uc2dc\ub098\ub9ac\uc624 \uc124\uba85')
    pdf.p('\uc774 \uc608\uc81c\uc5d0\uc11c\ub294:')
    pdf.bullets([
        'UAV 1\ub300 (ID: 400)\uac00 \ucd08\uae30 \uc704\uce58\uc5d0\uc11c \uc2dc\uc791',
        '\uc218\ub85c\ub97c \ub530\ub77c\uc11c \ub77c\uc778 \ud0d0\uc0c9 \uc784\ubb34 \uc218\ud589',
        'OpenAMASE \uc2dc\ubbac\ub808\uc774\ud130\uc5d0\uc11c UAV \ube44\ud589 \uc2dc\uac01\ud654',
        '\uce74\uba54\ub77c \uc9d0\ubc8c\uc774 \uc790\ub3d9\uc73c\ub85c \uc218\ub85c \ubc29\ud5a5\uc744 \ud5a5\ud568',
    ])

    pdf.subsec('\ub3d9\uc791 \ud750\ub984 \uc0c1\uc138')
    pdf.diagram('\uc218\ub85c \ud0d0\uc0c9 \uc608\uc81c \ub3d9\uc791 \ud750\ub984',
'''  1. AMASE: UAV 400 \ucd08\uae30\ud654 + \uc218\ub85c \uc9c0\ud615 \ub85c\ub4dc
  2. UxAS: AirVehicleConfiguration (UAV \uc0ac\uc591 \uc218\uc2e0)
  3. UxAS: AirVehicleState (UAV \ud604\uc7ac \uc704\uce58 \uc218\uc2e0)
  4. UxAS: LineOfInterest (\uc218\ub85c \uc88c\ud45c \uc815\uc758)
  5. UxAS: LineSearchTask (\ud0d0\uc0c9 \uc784\ubb34 \uc815\uc758)
  6. UxAS: OperatingRegion (\uc6b4\uc6a9 \uc601\uc5ed \uc815\uc758)
  7. UxAS: AutomationRequest (\uc784\ubb34 \uc2e4\ud589 \uc694\uccad)
     |
     v
  8. Validator -> UniqueAutomationRequest
  9. Task -> TaskPlanOptions (1\ub300 UAV\ub85c 1\uac00\uc9c0 \uc635\uc158)
  10. RouteAggregator -> CostMatrix
  11. BranchBound -> Assignment (UAV400 -> LineSearch)
  12. PlanBuilder -> MissionCommand (\uc6e8\uc774\ud3ec\uc778\ud2b8 \uc0dd\uc131)
     |
     v
  13. AMASE: UAV 400 \ube44\ud589 \uc2dc\uc791 \u2192 \uce74\uba54\ub77c \uc790\ub3d9 \uc81c\uc5b4''')

    pdf.sec('\uc608\uc81c 3: \ub2e4\uc911 UAV \uc218\ub85c \ud0d0\uc0c9')
    pdf.code('$ ./run-example 02b_Double_WaterwaySearch', '\uc2e4\ud589 \uba85\ub839')
    pdf.p('2\ub300\uc758 UAV\uac00 \uc218\ub85c \ud0d0\uc0c9 \uc784\ubb34\ub97c \ubd84\ub2f4\ud569\ub2c8\ub2e4. Branch & Bound \uc54c\uace0\ub9ac\uc998\uc774 \uac01 UAV\uc5d0 \uc5b4\ub5a4 \uc601\uc5ed\uc744 \ud560\ub2f9\ud560\uc9c0 \ucd5c\uc801\uc73c\ub85c \uacb0\uc815\ud569\ub2c8\ub2e4.')

    pdf.sec('\uc608\uc81c 4: \uc784\ubb34 \ud560\ub2f9 (AssignTasks)')
    pdf.code('$ ./run-example 05_AssignTasks', '\uc2e4\ud589 \uba85\ub839')
    pdf.p('\uc5ec\ub7ec \ub300\uc758 UAV\uc5d0 \ub2e4\uc591\ud55c \ud0dc\uc2a4\ud06c\ub97c \ud560\ub2f9\ud558\ub294 \uc608\uc81c\uc785\ub2c8\ub2e4. \uc601\uc5ed \ud0d0\uc0c9, \ub77c\uc778 \ud0d0\uc0c9, \uac10\uc2dc \ub4f1 \ub2e4\uc591\ud55c \ud0dc\uc2a4\ud06c\ub97c \uc870\ud569\ud558\uc5ec \ucd5c\uc801\uc758 \ud560\ub2f9\uc744 \uacc4\uc0b0\ud569\ub2c8\ub2e4.')

    pdf.sec('\uac1c\ubcc4 \ud0dc\uc2a4\ud06c \uc608\uc81c (99_Tasks)')
    pdf.p('examples/99_Tasks/ \ub514\ub809\ud1a0\ub9ac\uc5d0\ub294 \uac01 \ud0dc\uc2a4\ud06c \uc720\ud615\ubcc4 \ub3c5\ub9bd \uc608\uc81c\uac00 \uc788\uc2b5\ub2c8\ub2e4:')
    pdf.tbl(
        ['\ub514\ub809\ud1a0\ub9ac', '\ub0b4\uc6a9'],
        [
            ['AngledAreaSearchTask/', '\uac01\ub3c4 \uc9c0\uc815 \uc601\uc5ed \ud0d0\uc0c9'],
            ['CmasiAreaSearchTask/', 'CMASI \uc601\uc5ed \ud0d0\uc0c9 (\uc6d0/\ub2e4\uac01\ud615)'],
            ['CmasiLineSearchTask/', '\ub77c\uc778 \ud0d0\uc0c9'],
            ['CmasiPointSearchTask/', '\uc9c0\uc810 \ud0d0\uc0c9'],
            ['PatternSearchTask/', '\ud328\ud134 \ud0d0\uc0c9 (\ub098\uc120\ud615)'],
            ['BlockadeTask/', '\uc601\uc5ed \ubd09\uc1c4'],
            ['CordonTask/', '\ub458\ub808 \ubd09\uc1c4'],
            ['EscortTask/', '\ud638\uc704 \uc784\ubb34'],
            ['CommRelayTask/', '\ud1b5\uc2e0 \uc911\uacc4'],
            ['MultiVehicleWatchTask/', '\ub2e4\uc911 \ucc28\ub7c9 \uac10\uc2dc'],
        ],
        [65, 120]
    )


def write_chapter8(pdf):
    """Chapter 8: Multi-Vehicle Operations"""
    pdf.ch('\ub2e4\uc911 \ube44\ud589\uccb4 \uc6b4\uc6a9',
           'Multi-Vehicle Operations')

    pdf.sec('\ub2e4\uc911 UAV \ud560\ub2f9 \uc6d0\ub9ac')
    pdf.p('OpenUxAS\uc758 \ud575\uc2ec \uae30\ub2a5 \uc911 \ud558\ub098\ub294 \uc5ec\ub7ec \ub300\uc758 UAV\uc5d0 \uc784\ubb34\ub97c \ucd5c\uc801\uc73c\ub85c \ud560\ub2f9\ud558\ub294 \uac83\uc785\ub2c8\ub2e4.')
    pdf.diagram('\ub2e4\uc911 UAV \uc784\ubb34 \ud560\ub2f9 \ud504\ub85c\uc138\uc2a4',
'''  AutomationRequest
  {Vehicles: [V1, V2, V3], Tasks: [T1, T2, T3]}
      |
      v
  \u2460 \uac01 Task \uc11c\ube44\uc2a4: TaskPlanOptions \uc0dd\uc131
     T1: [V1\uc6a9_\uc635\uc158, V2\uc6a9_\uc635\uc158, V3\uc6a9_\uc635\uc158]
     T2: [V1\uc6a9_\uc635\uc158, V2\uc6a9_\uc635\uc158, V3\uc6a9_\uc635\uc158]
     T3: [V1\uc6a9_\uc635\uc158, V2\uc6a9_\uc635\uc158, V3\uc6a9_\uc635\uc158]
      |
      v
  \u2461 RouteAggregator: \ube44\uc6a9 \ud589\ub82c \uc0dd\uc131
     |  T1    T2    T3
  V1 | 3200  4100  2800
  V2 | 2900  3500  4200
  V3 | 4500  2700  3100
      |
      v
  \u2462 BranchBound: \ucd5c\uc801 \ud560\ub2f9 \uacc4\uc0b0 (MINMAX)
     V1 -> T3 (cost=2800)
     V2 -> T1 (cost=2900)
     V3 -> T2 (cost=2700)
     Max cost = 2900 (\ucd5c\uc18c\ud654\ub428)''')

    pdf.sec('\uc601\uc5ed \ubd84\ud560 \uc804\ub7b5')
    pdf.p('\ub113\uc740 \uc601\uc5ed\uc744 \uc5ec\ub7ec UAV\ub85c \ub098\ub204\uc5b4 \uac10\uc2dc\ud558\ub824\uba74, \uc601\uc5ed\uc744 \ubbf8\ub9ac \ubd84\ud560\ud558\uc5ec \ubcc4\ub3c4\uc758 \ud0dc\uc2a4\ud06c\ub85c \uc815\uc758\ud558\ub294 \ubc29\ubc95\uc774 \ud6a8\uacfc\uc801\uc785\ub2c8\ub2e4.')
    pdf.diagram('\uc601\uc5ed \ubd84\ud560 \uc804\ub7b5',
'''  \uc804\uccb4 \uc601\uc5ed:                  \ubd84\ud560 \ud6c4:
  +------------------+        +--------+--------+
  |                  |        | Task1  | Task2  |
  |   \ub113\uc740 \uac10\uc2dc     |   =>   | (UAV1) | (UAV2) |
  |   \uc601\uc5ed           |        |        |        |
  +------------------+        +--------+--------+

  \ubc29\ubc95:
  1. \uc601\uc5ed\uc744 UAV \uc218\ub9cc\ud07c AreaOfInterest\ub85c \ubd84\ud560
  2. \uac01 \uc601\uc5ed\uc5d0 \ub300\ud574 AngledAreaSearchTask \uc0dd\uc131
  3. AutomationRequest\uc5d0 \ubaa8\ub4e0 Task\uc640 Vehicle \ud3ec\ud568
  4. BranchBound\uac00 \ucd5c\uc801 \ud560\ub2f9 \uc790\ub3d9 \uacc4\uc0b0''')

    pdf.subsec('\uc601\uc5ed \ubd84\ud560 XML \uc608\uc2dc')
    pdf.code('''<!-- \uc601\uc5ed 1: \uc11c\ucabd \ubc18 -->
<AreaOfInterest><AreaID>1</AreaID>
  <Area><Polygon><BoundaryPoints>
    <!-- \uc11c\ucabd \uc601\uc5ed \uc88c\ud45c -->
  </BoundaryPoints></Polygon></Area>
</AreaOfInterest>

<!-- \uc601\uc5ed 2: \ub3d9\ucabd \ubc18 -->
<AreaOfInterest><AreaID>2</AreaID>
  <Area><Polygon><BoundaryPoints>
    <!-- \ub3d9\ucabd \uc601\uc5ed \uc88c\ud45c -->
  </BoundaryPoints></Polygon></Area>
</AreaOfInterest>

<!-- \ud0dc\uc2a4\ud06c 1: \uc11c\ucabd \uc601\uc5ed \ud0d0\uc0c9 -->
<AngledAreaSearchTask>
  <TaskID>1001</TaskID>
  <SearchAreaID>1</SearchAreaID>
</AngledAreaSearchTask>

<!-- \ud0dc\uc2a4\ud06c 2: \ub3d9\ucabd \uc601\uc5ed \ud0d0\uc0c9 -->
<AngledAreaSearchTask>
  <TaskID>1002</TaskID>
  <SearchAreaID>2</SearchAreaID>
</AngledAreaSearchTask>

<!-- \uc790\ub3d9\ud654 \uc694\uccad: 2\ub300 UAV, 2\uac1c \ud0dc\uc2a4\ud06c -->
<AutomationRequest>
  <EntityList><int64>400</int64><int64>500</int64></EntityList>
  <TaskList><int64>1001</int64><int64>1002</int64></TaskList>
  <OperatingRegion>100</OperatingRegion>
</AutomationRequest>''', '\ub2e4\uc911 UAV \uc601\uc5ed \ubd84\ud560 \uc124\uc815')

    pdf.sec('\uce74\uba54\ub77c \uae30\ubc18 \ub808\uc778 \uacc4\uc0b0')
    pdf.p('UAV\uc758 \uce74\uba54\ub77c \uc13c\uc11c\uc5d0 \ub530\ub77c \ud0d0\uc0c9 \ub808\uc778 \uac04\uaca9\uc774 \uc790\ub3d9\uc73c\ub85c \uacc4\uc0b0\ub429\ub2c8\ub2e4:')
    pdf.diagram('\uce74\uba54\ub77c \uc13c\uc11c \ud48b\ud504\ub9b0\ud2b8 \uae30\ubc18 \ub808\uc778 \uacc4\uc0b0',
'''  \uc785\ub825:
    - UAV \uace0\ub3c4: 700m
    - \uce74\uba54\ub77c FOV: 45 degree
    - GSD \uc694\uad6c: 0.5m/pixel
    - \uc870\uc0ac\uac01: -60 degree
      |
      v
  \uacc4\uc0b0:
    SensorManagerService \u2192 SensorFootprint
    widthCenter = 2 * 700 * tan(45/2) = ~580m
    laneSpacing = 580 * 0.9 = ~522m  (10% \uc624\ubc84\ub7a9)
      |
      v
  \uacb0\uacfc:
    522m \uac04\uaca9\uc73c\ub85c \ud3c9\ud589 \ub808\uc778 \uc0dd\uc131
    \uc601\uc5ed\ud3ed 5km -> \ub808\uc778 \uc218 = ceil(5000/522) = 10\uac1c \ub808\uc778''')


def write_chapter9(pdf):
    """Chapter 9: Results Analysis"""
    pdf.ch('\uacb0\uacfc \ubd84\uc11d',
           'Understanding Results')

    pdf.sec('\ucd9c\ub825 \ub514\ub809\ud1a0\ub9ac \uad6c\uc870')
    pdf.p('\uc608\uc81c\ub97c \uc2e4\ud589\ud558\uba74 RUNDIR_* \ub514\ub809\ud1a0\ub9ac\uc5d0 \uacb0\uacfc\uac00 \uc800\uc7a5\ub429\ub2c8\ub2e4:')
    pdf.code('''RUNDIR_WaterwaySearch/
\u251c\u2500\u2500 datawork/
\u2502   \u2514\u2500\u2500 SavedMessages/     # \uc2dc\uac04\uc21c \uba54\uc2dc\uc9c0 \ub85c\uadf8
\u251c\u2500\u2500 log/
\u2502   \u2514\u2500\u2500 uxas_log.csv       # \uc11c\ube44\uc2a4 \ub85c\uadf8
\u2514\u2500\u2500 output/
    \u2514\u2500\u2500 *.xml              # \ucd9c\ub825 \uba54\uc2dc\uc9c0''', '\uacb0\uacfc \ub514\ub809\ud1a0\ub9ac \uad6c\uc870')

    pdf.sec('\uba54\uc2dc\uc9c0 \ub85c\uadf8 \ubd84\uc11d')
    pdf.p('SavedMessages \ub514\ub809\ud1a0\ub9ac\uc5d0\ub294 \uc2dc\uc2a4\ud15c\uc5d0\uc11c \uad50\ud658\ub41c \ubaa8\ub4e0 LMCP \uba54\uc2dc\uc9c0\uac00 \uc2dc\uac04\uc21c\uc73c\ub85c \uc800\uc7a5\ub429\ub2c8\ub2e4. \uc774\ub97c \ubd84\uc11d\ud558\uba74 \uc2dc\uc2a4\ud15c\uc758 \ub3d9\uc791\uc744 \uc0c1\uc138\ud788 \uc774\ud574\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.')
    pdf.p('\uc8fc\uc694 \ud655\uc778 \ud56d\ubaa9:')
    pdf.tbl(
        ['\uba54\uc2dc\uc9c0', '\ud655\uc778 \ub0b4\uc6a9'],
        [
            ['UniqueAutomationRequest', '\uc694\uccad\uc774 \uc815\uc0c1 \uc0dd\uc131\ub418\uc5c8\ub294\uc9c0'],
            ['TaskPlanOptions', '\uac01 \ud0dc\uc2a4\ud06c\uc758 \uc635\uc158\uacfc \ube44\uc6a9'],
            ['AssignmentCostMatrix', '\ube44\uc6a9 \ud589\ub82c \ub0b4\uc6a9'],
            ['TaskAssignmentSummary', '\ucd5c\uc885 \ud560\ub2f9 \uacb0\uacfc'],
            ['MissionCommand', '\uc0dd\uc131\ub41c \uc6e8\uc774\ud3ec\uc778\ud2b8 \uc218'],
            ['AirVehicleState', 'UAV \uc704\uce58/\uc18d\ub3c4 \ubcc0\ud654'],
        ],
        [65, 120]
    )

    pdf.sec('OpenAMASE \uc2dc\uac01\ud654')
    pdf.p('OpenAMASE\ub294 Java \uae30\ubc18 \uc2dc\ubbac\ub808\uc774\ud130\ub85c, \ub2e4\uc74c\uc744 \uc2dc\uac01\uc801\uc73c\ub85c \ud655\uc778\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4:')
    pdf.bullets([
        'UAV\uc758 \uc2e4\uc2dc\uac04 \uc704\uce58\uc640 \ube44\ud589 \uacbd\ub85c',
        '\uc6e8\uc774\ud3ec\uc778\ud2b8 \uacbd\ub85c (\ud30c\ub780\uc120)',
        '\uce74\uba54\ub77c \uc9d0\ubc8c\uc758 \uc870\uc900\uc810 (\ub179\uc0c9 \uc810)',
        '\ud0d0\uc0c9 \uc601\uc5ed \uacbd\uacc4 (\ub178\ub780\uc120)',
        '\ube44\ud589 \uae08\uc9c0/\ud5c8\uc6a9 \uc601\uc5ed',
        'UAV \uc0c1\ud0dc \uc815\ubcf4 (\uc18d\ub3c4, \uace0\ub3c4, \ubc29\ud5a5)',
    ])

    pdf.sec('\uc131\ub2a5 \uc9c0\ud45c')
    pdf.p('\uc784\ubb34 \uc218\ud589 \uc131\ub2a5\uc744 \ud3c9\uac00\ud558\ub294 \uc8fc\uc694 \uc9c0\ud45c:')
    pdf.tbl(
        ['\uc9c0\ud45c', '\uc124\uba85', '\uce21\uc815 \ubc29\ubc95'],
        [
            ['\ud560\ub2f9 \uc2dc\uac04', 'Request~Assignment \uc18c\uc694\uc2dc\uac04', '\uba54\uc2dc\uc9c0 \ud0c0\uc784\uc2a4\ud0ec\ud504'],
            ['\uc784\ubb34 \uc644\ub8cc\uc728', '\ud560\ub2f9\ub41c \uc784\ubb34 \uc911 \uc644\ub8cc \ube44\uc728', 'TaskComplete \uba54\uc2dc\uc9c0'],
            ['\uacbd\ub85c \ud6a8\uc728', '\uc2e4\uc81c\uacbd\ub85c/\uc9c1\uc120\uacbd\ub85c \ube44\uc728', '\uc6e8\uc774\ud3ec\uc778\ud2b8 \ubd84\uc11d'],
            ['\uc601\uc5ed \ucee4\ubc84\ub9ac\uc9c0', '\ud0d0\uc0c9\ub41c \uba74\uc801/\uc804\uccb4 \uba74\uc801', '\uc13c\uc11c \ud48b\ud504\ub9b0\ud2b8 \ub204\uc801'],
            ['\ubd80\ud558 \uade0\ud615', '\uac01 UAV \ube44\ud589\uc2dc\uac04 \ud3b8\ucc28', 'MINMAX \ube44\uc6a9 \ubd84\uc11d'],
        ],
        [40, 75, 70]
    )

    pdf.sec('\ub514\ubc84\uae45 \ud301')
    pdf.p('\ubb38\uc81c \ud574\uacb0\uc744 \uc704\ud55c \ub514\ubc84\uae45 \ubc29\ubc95:')
    pdf.bullets([
        '\uba54\uc2dc\uc9c0 \ub85c\uadf8 \ud655\uc778: SavedMessages \ub514\ub809\ud1a0\ub9ac\uc758 \uc2dc\uac04\uc21c \uba54\uc2dc\uc9c0 \ud655\uc778',
        'AutomationDiagram \uc11c\ube44\uc2a4: \uba54\uc2dc\uc9c0 \ud750\ub984\uc744 \uc2dc\uac01\uc801\uc73c\ub85c \ud45c\uc2dc',
        'uxas_log.csv: \uac01 \uc11c\ube44\uc2a4\uc758 \ub3d9\uc791 \ub85c\uadf8 \ud655\uc778',
        'AMASE \uc2dc\ubbac\ub808\uc774\ud130: \uc2e4\uc2dc\uac04 \ube44\ud589 \uc0c1\ud0dc \ud655\uc778',
    ])


def write_chapter10(pdf):
    """Chapter 10: Advanced Topics"""
    pdf.ch('\uace0\uae09 \uc8fc\uc81c',
           'Advanced Topics')

    pdf.sec('\uc0c8 \uc11c\ube44\uc2a4 \uac1c\ubc1c\ud558\uae30')
    pdf.p('\uc0c8\ub85c\uc6b4 \uc11c\ube44\uc2a4\ub97c \ub9cc\ub4e4\ub824\uba74 ServiceBase\ub97c \uc0c1\uc18d\ubc1b\ub294 \ud074\ub798\uc2a4\ub97c \uc791\uc131\ud569\ub2c8\ub2e4:')
    pdf.code('''// MyCustomService.h
#include "ServiceBase.h"

class MyCustomService : public ServiceBase {
public:
    // \uc790\ub3d9 \ub4f1\ub85d\uc744 \uc704\ud55c \ub9e4\ud06c\ub85c
    static ServiceBase::CreationRegistrar<MyCustomService>
        s_registrar;

    // \uc11c\ube44\uc2a4 \uc774\ub984 (\uc124\uc815 XML\uc5d0\uc11c \uc0ac\uc6a9)
    static const std::string s_typeName() {
        return "MyCustomService";
    }

    // \uc0dd\uba85\uc8fc\uae30 \uba54\uc11c\ub4dc
    bool configure(const pugi::xml_node& ndComponent) override;
    bool initialize() override;
    bool start() override;
    bool terminate() override;

    // \uba54\uc2dc\uc9c0 \ucc98\ub9ac
    bool processReceivedLmcpMessage(
        std::unique_ptr<uxas::communications::data::LmcpMessage>
            receivedLmcpMessage) override;
};''', '\uc11c\ube44\uc2a4 \ud074\ub798\uc2a4 \ud15c\ud50c\ub9bf')
    pdf.p('\ud575\uc2ec \ub2e8\uacc4:')
    pdf.bullets([
        'ServiceBase \uc0c1\uc18d + CreationRegistrar\ub85c \uc790\ub3d9 \ub4f1\ub85d',
        'configure(): XML \uc124\uc815 \ud30c\uc2f1',
        'initialize(): \ucd08\uae30\ud654 + addSubscriptionAddress()\ub85c \uad00\uc2ec \uba54\uc2dc\uc9c0 \uad6c\ub3c5',
        'processReceivedLmcpMessage(): \uc218\uc2e0 \uba54\uc2dc\uc9c0 \ucc98\ub9ac',
        'sendLmcpObjectBroadcastMessage(): \uba54\uc2dc\uc9c0 \ubc1c\uc1a1',
    ])

    pdf.sec('\uc0c8 \ud0dc\uc2a4\ud06c \uac1c\ubc1c\ud558\uae30')
    pdf.p('\uc0c8\ub85c\uc6b4 \ud0dc\uc2a4\ud06c\ub97c \ub9cc\ub4e4\ub824\uba74 TaskServiceBase\ub97c \uc0c1\uc18d\ubc1b\uc2b5\ub2c8\ub2e4. \ud575\uc2ec\uc740 buildTaskPlanOptions() \uba54\uc11c\ub4dc\ub97c \uad6c\ud604\ud558\ub294 \uac83\uc785\ub2c8\ub2e4:')
    pdf.bullets([
        'configureTask(): \ud0dc\uc2a4\ud06c \ud30c\ub77c\ubbf8\ud130 \ud30c\uc2f1',
        'buildTaskPlanOptions(): \uac01 \ucc28\ub7c9\uc5d0 \ub300\ud55c \ud0dc\uc2a4\ud06c \uc635\uc158 \uc0dd\uc131 (\ud575\uc2ec!)',
        'processReceivedLmcpMessageTask(): \ud0dc\uc2a4\ud06c \ud2b9\ud654 \uba54\uc2dc\uc9c0 \ucc98\ub9ac',
        'activeEntityState(): \ud560\ub2f9\ub41c \ucc28\ub7c9 \uc0c1\ud0dc \uc5c5\ub370\uc774\ud2b8 \uc2dc \ud638\ucd9c',
    ])

    pdf.sec('\ubd84\uc0b0 \uc2dc\uc2a4\ud15c \uad6c\uc131')
    pdf.p('OpenUxAS\ub294 \uc5ec\ub7ec UxAS \uc778\uc2a4\ud134\uc2a4\ub97c \ub124\ud2b8\uc6cc\ud06c\ub85c \uc5f0\uacb0\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. LmcpObjectNetworkTcpBridge\ub97c \uc0ac\uc6a9\ud558\uc5ec TCP \uc5f0\uacb0\uc744 \uc124\uc815\ud569\ub2c8\ub2e4:')
    pdf.code('''<!-- \uc11c\ubc84 \uce21 (EntityID=100) -->
<Bridge Type="LmcpObjectNetworkTcpBridge"
        TcpAddress="tcp://*:5555" Server="TRUE">
  <SubscribeToMessage
      MessageType="afrl.cmasi.AirVehicleState"/>
</Bridge>

<!-- \ud074\ub77c\uc774\uc5b8\ud2b8 \uce21 (EntityID=200) -->
<Bridge Type="LmcpObjectNetworkTcpBridge"
        TcpAddress="tcp://192.168.1.100:5555"
        Server="FALSE">
  <SubscribeToMessage
      MessageType="afrl.cmasi.MissionCommand"/>
</Bridge>''', '\ubd84\uc0b0 \uc2dc\uc2a4\ud15c \ube0c\ub9ac\uc9c0 \uc124\uc815')

    pdf.sec('\uc131\ub2a5 \ud29c\ub2dd')
    pdf.p('\ub300\uaddc\ubaa8 \uc2dc\ub098\ub9ac\uc624\uc5d0\uc11c\uc758 \uc131\ub2a5 \ucd5c\uc801\ud654 \ud301:')
    pdf.bullets([
        'NumberNodesMaximum: Branch & Bound \ud0d0\uc0c9 \ub178\ub4dc \uc81c\ud55c\uc73c\ub85c \uc18d\ub3c4 \ud5a5\uc0c1 (0=\ubb34\uc81c\ud55c)',
        'MaxResponseTime_ms: Validator \ud0c0\uc784\uc544\uc6c3 \uc870\uc815',
        '\ud0dc\uc2a4\ud06c \uc601\uc5ed \ud06c\uae30 \ucd5c\uc801\ud654: \ub108\ubb34 \ud070 \uc601\uc5ed\uc740 \uc6e8\uc774\ud3ec\uc778\ud2b8\uac00 \ub9ce\uc544\uc838 \ub290\ub824\uc9d0',
        'UAV \uc218 vs \ud0dc\uc2a4\ud06c \uc218: \uc870\ud569\uc774 \ub9ce\uc544\uc9c0\uba74 \ud560\ub2f9 \uc2dc\uac04 \uc99d\uac00',
    ])

    pdf.sec('\uc6a9\uc5b4 \uc0ac\uc804 (Glossary)')
    pdf.tbl(
        ['\uc6a9\uc5b4', '\uc601\ubb38', '\uc124\uba85'],
        [
            ['UAV', 'Unmanned Aerial Vehicle', '\ubb34\uc778 \ud56d\uacf5\uae30'],
            ['LMCP', 'Lightweight Message Control Protocol', '\uacbd\ub7c9 \uba54\uc2dc\uc9c0 \ud504\ub85c\ud1a0\ucf5c'],
            ['CMASI', 'Common Mission Automation Services Interface', '\uc784\ubb34 \uc790\ub3d9\ud654 \ud45c\uc900 \uc778\ud130\ud398\uc774\uc2a4'],
            ['MDM', 'Message Definition Model', '\uba54\uc2dc\uc9c0 \uc815\uc758 \ubaa8\ub378'],
            ['FOV', 'Field of View', '\uc2dc\uc57c\uac01'],
            ['GSD', 'Ground Sample Distance', '\uc9c0\uc0c1 \uc0d8\ud50c \uac70\ub9ac'],
            ['B&B', 'Branch and Bound', '\ubd84\uc9c0\ud55c\uc815 \uc54c\uace0\ub9ac\uc998'],
            ['DPSS', 'Dynamic Perimeter Surveillance', '\ub3d9\uc801 \ub458\ub808 \uac10\uc2dc \uc2dc\uc2a4\ud15c'],
            ['AMASE', 'Air Mobility Autonomy Sim Environment', 'UAV \uc2dc\ubbac\ub808\uc774\ud130'],
            ['MAS', 'Multi-Agent System', '\ub2e4\uc911 \uc5d0\uc774\uc804\ud2b8 \uc2dc\uc2a4\ud15c'],
        ],
        [20, 80, 85]
    )
