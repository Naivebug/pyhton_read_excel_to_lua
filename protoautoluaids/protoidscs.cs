
using Google.Protobuf;
using System.Collections.Generic;
namespace protos
{
	class protoids
	{
		delegate object Fn(byte[] data);
		static Dictionary<int, string> idnames = new Dictionary<int, string>(){
			[257] = "Protocol.C2SLogin",
			[258] = "Protocol.S2CHello",
			[259] = "Protocol.S2CLoginSuccess",
			[260] = "Protocol.C2SChangePetName",
			[261] = "Protocol.S2CPetDataAdd",
			[262] = "Protocol.S2COnePet",
			[263] = "Protocol.S2CAddPet",
			[264] = "Protocol.S2CMorePet",
		};
		static Dictionary<string,int> nameids = new Dictionary<string, int>(){
			["Protocol.C2SLogin"] = 257,
			["Protocol.S2CHello"] = 258,
			["Protocol.S2CLoginSuccess"] = 259,
			["Protocol.C2SChangePetName"] = 260,
			["Protocol.S2CPetDataAdd"] = 261,
			["Protocol.S2COnePet"] = 262,
			["Protocol.S2CAddPet"] = 263,
			["Protocol.S2CMorePet"] = 264,
		};
		static Dictionary<int, Fn> ids = new Dictionary<int, Fn>(){
			[257] = Protocol.C2SLogin.Parser.ParseFrom,
			[258] = Protocol.S2CHello.Parser.ParseFrom,
			[259] = Protocol.S2CLoginSuccess.Parser.ParseFrom,
			[260] = Protocol.C2SChangePetName.Parser.ParseFrom,
			[261] = Protocol.S2CPetDataAdd.Parser.ParseFrom,
			[262] = Protocol.S2COnePet.Parser.ParseFrom,
			[263] = Protocol.S2CAddPet.Parser.ParseFrom,
			[264] = Protocol.S2CMorePet.Parser.ParseFrom,
		};
	}
}