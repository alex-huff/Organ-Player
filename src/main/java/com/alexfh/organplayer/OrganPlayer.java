package com.alexfh.organplayer;

import com.alexfh.organplayer.server.PlayerServer;
import net.fabricmc.api.ModInitializer;
import net.minecraft.client.MinecraftClient;

public
class OrganPlayer implements ModInitializer
{

    public static MinecraftClient mc = MinecraftClient.getInstance();

    @Override
    public
    void onInitialize()
    {
        new PlayerServer().start();
    }

}
