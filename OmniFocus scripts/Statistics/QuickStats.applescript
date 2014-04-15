property pTitle : "OmniFocus: Quick Stats"
property pVersion : "2.07"

property pstrDBPath : "$HOME/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2"
property pstrMinOSX : "10.6"

property pTimeOut : 20

-- Ver 0.8 adds clipboard option to dialogue
-- Ver 0.9 gives an error message if the cache schema has changed, leading to an SQL error in the script
-- Ver 1.0 slight simplification of the code
-- Ver 1.1 added count of Pending projects
-- Ver 1.2 added a count of available actions
-- Ver 1.3 added a break-down of unavailable actions
-- Ver 1.4 added count of Current projects to complement Pending projects
-- ver 1.5 replaced Applescript time function with SQL time expression
-- Ver 1.7 Reorganizes menu, and attempts to enable access for .macappstore installations of OF
--Ver 1.8 Adjusts handling of variant bundle identifiers generally
-- Ver 2.00 Redraft of task breakdown, with progressive narrowing of criteria ...

property pToClipboard : "Copy list to clipboard"

if not FileExists(pstrDBPath) then set pstrDBPath to GetCachePath()

tell application "Finder"
	if (version < pstrMinOSX) then
		display dialog "This script requires OSX " & pstrMinOSX & " or higher" buttons {"OK"} default button 1 with title pTitle & "Ver. " & pVersion
		return
	end if
end tell

if pstrDBPath ­ "" then
	set strCmd to "sqlite3 -separator ': ' \"" & pstrDBPath & "\" " & quoted form of ("
	select \"INBOX GROUPS & ACTIONS\", count(*) from task where (inInbox=1);
	select \"    Inbox action groups\", count(*) from task where (inInbox=1) and (childrenCount>0);
	select \"    Inbox actions\", count(*) from task where (inInbox=1) and (childrenCount=0);
	select null;
	select \"FOLDERS\"	, count(*) from folder;
	select \"    Active folders\", count(*) from folder where effectiveActive=1;
	select \"    Dropped folders\", count(*) from folder where effectiveActive=0;
	select null;
	select \"PROJECTS\", count(*) from projectInfo where containsSingletonActions=0;
	select \"    Active projects\", count(*) from projectInfo where (containsSingletonActions=0) and (status=\"active\");
	select \"            Current projects\", count(*) from projectInfo p join task t on t.projectinfo=p.pk where (p.containsSingletonActions=0) and (p.folderEffectiveActive=1) and (p.status=\"active\") and (t.dateToStart is null or t.dateToStart < (strftime('%s','now') - strftime('%s','2001-01-01')));
	select \"            Pending projects\", count(*) from projectInfo p join task t on t.projectinfo=p.pk where (p.containsSingletonActions=0) and (p.folderEffectiveActive=1) and (p.status=\"active\") and (t.dateToStart > (strftime('%s','now') - strftime('%s','2001-01-01')));
	select \"    On-hold projects\", count(*) from projectInfo where (containsSingletonActions=0) and (status=\"inactive\");
	select \"    Completed projects\", count(*) from projectInfo where (containsSingletonActions=0) and (status=\"done\");
	select \"    Dropped projects\", count(*) from projectInfo where (containsSingletonActions=0) and (( status=\"dropped\") or (folderEffectiveActive=0));
	select null;	
	select \"SINGLE ACTION LISTS\", count(*) from projectInfo where containsSingletonActions=1;
	select \"    Active single action lists\", count(*) from projectInfo where (containsSingletonActions=1) and (status=\"active\");
	select \"    On-hold single action lists\", count(*) from projectInfo where (containsSingletonActions=1) and (status=\"inactive\");
	select \"    Completed single action lists\", count(*) from projectInfo where (containsSingletonActions=1) and (status=\"done\");
	select \"    Dropped single action lists\", count(*) from projectInfo where (containsSingletonActions=1) and (( status=\"dropped\") or (folderEffectiveActive=0));
	select null;
	select \"CONTEXTS\", count(*) from context;
	select \"    Active contexts\", count(*) from context where (effectiveActive=1) and (allowsNextAction=1);
	select \"    On-hold contexts\", count(*) from context where (effectiveActive=1) and allowsNextAction=0;
	select \"    Dropped contexts\", count(*) from context where effectiveActive=0;
	select null;
	select \"ACTION GROUPS\", count(*) from task where (projectinfo is null) and (childrenCount>0);
	select \"    Remaining action groups\", count(*) from task where (projectinfo is null) and (dateCompleted is null) and (childrenCount>0);
	select \"    Completed action groups\", count(dateCompleted) from task where (projectinfo is null) and (childrenCount>0);
	select null;
	select \"ACTIONS\", count(*) from task where (projectinfo is null) and (childrenCount=0);
	select \"    Completed actions\", count(dateCompleted) from task where (projectinfo is null) and (childrenCount=0);
	select \"    Dropped project actions\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp where (projectinfo is null) and (childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is not null and (tp.status=\"dropped\" or tp.folderEffectiveActive=0));
	select \"    Dropped context actions\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and c.effectiveActive= 0;
	select \"    Remaining actions\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1);
	select \"        Actions in Projects on hold\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is not null and tp.status=\"inactive\");
	select \"        Actions in Contexts on hold\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is null or tp.status!=\"inactive\")
				and (tp.context is not null and c.allowsNextAction=0);
	select \"        Blocked actions\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is null or tp.status!=\"inactive\")
				and (tp.context is null or c.allowsNextAction=1)
				and tp.blocked=1;
	select \"        	Blocked by future start date\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is null or tp.status!=\"inactive\")
				and (tp.context is null or c.allowsNextAction=1)
				and tp.blocked=1
				and tp.blockedByFutureStartDate=1;
	select \"        	Sequentially blocked\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is null or tp.status!=\"inactive\")
				and (tp.context is null or c.allowsNextAction=1)
				and tp.blocked=1
				and tp.blockedByFutureStartDate=0;
	select \"        Available actions\", count(*) from (task t left join projectinfo p on t.containingProjectinfo=p.pk) tp left join context c on tp.context=c.persistentIdentifier where (projectinfo is null) and (tp.childrenCount=0)  and (dateCompleted is null) 
				and (tp.containingProjectinfo is null or (tp.status !=\"dropped\" and tp.folderEffectiveActive=1))
				and (tp.context is null or c.effectiveActive= 1)
				and (tp.containingProjectInfo is null or tp.status!=\"inactive\")
				and (tp.context is null or c.allowsNextAction=1)
				and tp.blocked=0;
				
	")
	
	-- 		try
	set strList to do shell script strCmd
	-- 		on error
	-- 			display dialog "The SQL schema for the OmniFocus cache may have changed in a recent update of OF." & return & return & Â
	-- 				"Look on the OmniFocus user forums for an updated version of this script." buttons {"OK"} with title pTitle & "Ver. " & pVersion
	-- 			return
	-- 		end try
	tell application id "sevs"
		activate
		if button returned of (display dialog strList buttons {pToClipboard, "OK"} default button "OK" giving up after pTimeOut with title pTitle & " Ver. " & pVersion) Â
			is pToClipboard then tell application id "com.apple.finder" to set the clipboard to strList
	end tell
else
	tell application id "sevs"
		activate
		display dialog "OmniFocus cache not found ..." buttons {"OK"} default button 1 with title pTitle & " Ver. " & pVersion
	end tell
end if


on FileExists(strPath)
	(do shell script "test -e " & strPath & " ; echo $?") = "0"
end FileExists

on GetCachePath()
	try
		tell application "Finder" to tell (application file id "OFOC") to "$HOME/Library/Caches/" & its id & "/OmniFocusDatabase2"
	on error
		error "OmniFocus not installed ..."
	end try
end GetCachePath

