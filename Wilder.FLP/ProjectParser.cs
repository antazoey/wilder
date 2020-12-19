using System.IO;
using System.Text;
using Wilder.Common.Model;
using Wilder.FLP.Subparsers;

namespace Wilder.FLP
{
    internal class ProjectParser
    {
        readonly Project _project;
        Channel _currentChannel;
        Insert _currentInsert;
        InsertSlot _currentSlot;
        Pattern _currentPattern;
        int _versionMajor;

        public ProjectParser()
        {
            _project = new Project();
            _currentInsert = _project.Inserts[0];
        }

        public Project Project => _project;

        public GeneratorData GeneratorData => _currentChannel?.Data as GeneratorData;

        public AutomationData AutomationData => _currentChannel?.Data as AutomationData;

        public void ParseAutomationChannels(BinaryReader reader, long dataEnd)
        {
            AutomationParser.ParseAutomationChannels(_project, reader, dataEnd);
        }

        public void ParseAutomationData(BinaryReader reader, AutomationData autData)
        {
            AutomationParser.ParseAutomationData(_project, reader, autData);
        }

        public int CurrentChannel
        {
            set { _currentChannel = _project.Channels[value]; }
        }

        public uint CurrentChannelColor
        {
            set
            {
                if (_currentChannel != null)
                    _currentChannel.Color = value;
            }
        }

        public uint CurrentChannelMiddleNote
        {
            set
            {
                if (_currentChannel != null && _currentChannel.Data is GeneratorData genData)
                    genData.BaseNote = value + 9;
            }
        }

        public string CurrentChannelName
        {
            set
            {
                if (_currentChannel != null)
                    _currentChannel.Name = value;
            }
        }

        public void AddChannelFromIndex(int index)
        {
            ChannelParser.AddNewChannelFromIndex(_project, index);
        }

        public ushort CurrentInsertIcon { set { _currentInsert.Icon = value; } }

        public uint CurrentInsertColor { set { _currentInsert.Color = value; } }

        public void ParseInsertParameters(BinaryReader reader, long dataEnd)
        {
            InsertParser.ParseInsertParameters(_project, reader, dataEnd);
        }

        public void ParseInsertRoutes(BinaryReader reader)
        {
            InsertParser.ParseInsertRoutes(reader, _currentInsert);
            var newIndex = _currentInsert.Id + 1;
            if (newIndex < _project.Inserts.Length)
                _currentInsert = _project.Inserts[newIndex];
        }

        public void ParseInsertFlags(BinaryReader reader)
        {
            InsertParser.ParseInsertFlags(reader, _currentInsert);
            _currentSlot = new InsertSlot();  // New insert route, create new slot
        }

        public void ParseGeneratorName(GeneratorData genData, string name)
        {
            if (genData == null)
                return;
            genData.SampleFileName = name;
            genData.GeneratorName = "Sampler";
        }

        public string CurrentInsertName
        {
            set { _currentInsert.Name = value; }
        }

        public int CurrentPattern
        {
            set { _currentPattern = _project.Patterns[value - 1]; }
        }

        public string CurrentPatternName
        {
            set
            {
                if (_currentPattern != null)
                    _currentPattern.Name = value;
            }
        }

        public int CurrentSlot
        {
            set
            {
                if (_currentSlot != null) // Current slot after plugin event, now re-arranged.
                {
                    _currentInsert.Slots[value] = _currentSlot;
                    _currentSlot = new InsertSlot();
                }
                _currentChannel = null;
            }
        }

        public void ParsePatternNotes(BinaryReader reader, long dataEnd)
        {
            PatternNotesParser.ParsePatternNotes(_project, reader, _currentPattern, dataEnd);
        }

        public int PatternsCount => _project.Patterns.Count;

        public void AddPatternFromCount()
            => _project.Patterns.Add(new Pattern { Id = PatternsCount });


        public void ParsePlayListItems(BinaryReader reader, long dataEnd)
        {
            PlaylistParser.ParsePlayListItems(_project, reader, _versionMajor, dataEnd);
        }

        public void InitSlotPlugins(BinaryReader reader, GeneratorData genData, int bufferLength)
        {
            SlotPluginsParser.InitSlotPlugins(reader, genData, _currentSlot, bufferLength);
        }

        public void ParseVersion(byte[] bytes)
        {
            _project.VersionString = Encoding.UTF8.GetString(bytes);
            if (_project.VersionString.EndsWith("\0"))
            {
                var endIndex = _project.VersionString.Length - 1;
                _project.VersionString = _project.VersionString.Substring(0, endIndex);
            }
            var numbers = _project.VersionString.Split('.');
            _versionMajor = int.Parse(numbers[0]);
            _project.Version = (int.Parse(numbers[0]) << 8) +
                               (int.Parse(numbers[1]) << 4) +
                               (int.Parse(numbers[2]) << 0);
        }
    }
}
