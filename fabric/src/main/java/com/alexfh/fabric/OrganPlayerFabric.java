package com.alexfh.fabric;

import com.alexfh.OrganPlayer;
import net.fabricmc.api.ModInitializer;

public
class OrganPlayerFabric implements ModInitializer
{
    @Override
    public
    void onInitialize()
    {
        OrganPlayer.init();
    }
}
