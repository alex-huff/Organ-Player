package com.alexfh;

import com.alexfh.server.PlayerServer;
import net.minecraft.client.MinecraftClient;

public
class OrganPlayer
{
    public static final String          MOD_ID = "organplayer";
    public static final MinecraftClient mc     = MinecraftClient.getInstance();

    public static
    void init()
    {
        new PlayerServer().start();
    }
}
