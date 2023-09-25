package com.alexfh.organ;

import com.alexfh.OrganPlayer;
import net.minecraft.client.network.ClientPlayerEntity;
import net.minecraft.client.network.ClientPlayerInteractionManager;
import net.minecraft.command.argument.EntityAnchorArgumentType;
import net.minecraft.util.Hand;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.math.Vec3d;

public
class Organ
{

    private static final Vec3d     topLeftCorner       = new Vec3d(-92, 63, -11);
    private static final Vec3d     downDirection       = new Vec3d(1, 0, 0);
    private static final Vec3d     rightDirection      = new Vec3d(0, 0, -1);
    private static final int       monitorWidth        = 5;
    private static final int       monitorHeight       = 5;
    private static final int       screenPixelWidth    = 100;
    private static final int       screenPixelHeight   = 67;
    private static final int       xMargin             = 5;
    private static final int       yOuterMargin        = 5;
    private static final int       yInnerMargin        = 3;
    private static final int       noteBaseWidth       = 11;
    private static final int       noteStemWidth       = 6;
    private static final int       noteBaseHeight      = 6;
    private static final int       noteStemHeight      = 11;
    private static final int       noteHeight          = Organ.noteBaseHeight + Organ.noteStemHeight;
    private static final Vec3d     downRightDirection  = downDirection.add(rightDirection);
    private static final Vec3d     origin              = Organ.topLeftCorner.add(
        Organ.downRightDirection.multiply(1 / 8d));
    private static final double    realScreenWidth     = Organ.monitorWidth - 1 / 4d;
    private static final double    realScreenHeight    = Organ.monitorHeight - 1 / 4d;
    private static final double    halfPixelRealWidth  = Organ.realScreenWidth / (2 * Organ.screenPixelWidth);
    private static final double    halfPixelRealHeight = Organ.realScreenHeight / (2 * Organ.screenPixelHeight);
    private static final Vec3d[][] noteWorldPositions  = new Vec3d[3][13];

    static
    {
        for (int octave = 0; octave < 3; octave++)
        {
            for (int note = 0; note < 13; note++)
            {
                int screenX = Organ.xMargin + 1 + note * (Organ.noteStemWidth + 1) + Organ.noteStemWidth / 2;
                int screenY = Organ.yOuterMargin + 1 + (3 - (octave + 1)) * (Organ.noteHeight + Organ.yInnerMargin) +
                              Organ.noteStemHeight / 2;
                Organ.noteWorldPositions[octave][note] = Organ.screenSpaceToWorldSpace(screenX, screenY);
            }
        }
    }

    private static
    Vec3d screenSpaceToWorldSpace(int x, int y)
    {
        return Organ.origin.add(Organ.rightDirection.multiply(
            ((x - 1) / (double) Organ.screenPixelWidth) * Organ.realScreenWidth + Organ.halfPixelRealWidth).add(
            Organ.downDirection.multiply(
                ((y - 1) / (double) Organ.screenPixelHeight) * Organ.realScreenHeight + Organ.halfPixelRealHeight)));
    }

    public static
    void playNote(boolean pressed, int octave, int note)
    {
        OrganPlayer.mc.execute(() -> Organ.clickAt(Organ.noteWorldPositions[octave][note]));
    }

    public static
    void clickAt(Vec3d position)
    {
        ClientPlayerEntity player = OrganPlayer.mc.player;
        if (player == null)
        {
            return;
        }
        player.lookAt(EntityAnchorArgumentType.EntityAnchor.EYES, position);
        OrganPlayer.mc.gameRenderer.updateTargetedEntity(OrganPlayer.mc.getTickDelta());
        if (OrganPlayer.mc.crosshairTarget instanceof BlockHitResult blockHitResult)
        {
            ClientPlayerInteractionManager interactionManager = OrganPlayer.mc.interactionManager;
            if (interactionManager == null)
            {
                return;
            }
            interactionManager.interactBlock(player, Hand.MAIN_HAND, blockHitResult);
        }
    }

}
