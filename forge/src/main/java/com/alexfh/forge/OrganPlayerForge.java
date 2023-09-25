package com.alexfh.forge;

import com.alexfh.OrganPlayer;
import dev.architectury.platform.forge.EventBuses;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(OrganPlayer.MOD_ID)
public
class OrganPlayerForge
{
    public
    OrganPlayerForge()
    {
        EventBuses.registerModEventBus(OrganPlayer.MOD_ID, FMLJavaModLoadingContext.get().getModEventBus());
        OrganPlayer.init();
    }
}
