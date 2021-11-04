from Models.Subject import Subject, GameMode

gameMode = GameMode("mode", "level", "feedBack", "distraction")
subject = Subject("AT_00002", "Name", "kana",
                                  1992, 12,
                                  1,
                                  "sex", 1.5, 2.5, 3.5, "handOrFoot", "leftOrRight", "comment", gameMode)

subject.saveToDatabase()